#!/usr/bin/env python3
"""
Macau Event Inclusivity Scorer
Analyzes event accessibility using ML and spatial data
"""

import pandas as pd
import numpy as np
import json
import torch
import yaml
import argparse
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.spatial import cKDTree
import pickle
import glob
import warnings
warnings.filterwarnings('ignore')


class EventInclusivityScorer:
    def __init__(self, config_path='config.yaml'):
        """Initialize scorer with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        self._load_model()
        self._load_spatial_data()
        self._build_indices()
    
    def _load_model(self):
        """Load RoBERTa model and label mappings"""
        print("Loading ML model...")
        model_dir = self.config['model']['directory']
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.model.to(self.device)
        self.model.eval()
        
        with open(self.config['model']['label_mappings'], 'rb') as f:
            self.label_mappings = pickle.load(f)
        
        self.reverse_mappings = {}
        for category in ['activity_level', 'complexity', 'cost', 
                         'noise_level', 'cultural_type', 'audience_scope']:
            self.reverse_mappings[category] = {
                idx: label for label, idx in self.label_mappings[category].items()
            }
        
        print("✓ Model loaded")
    
    def _load_spatial_data(self):
        """Load parking, traffic, and bus stop data"""
        print("Loading spatial data...")
        
        # Parking
        self.parking_df = pd.read_csv(self.config['data']['parking'])
        self.parking_lookup = dict(zip(
            self.parking_df['name'].fillna('').astype(str).str.strip(),
            self.parking_df['category'].fillna('unknown')
        ))
        
        if 'latitude' in self.parking_df.columns:
            self.parking_coords = self.parking_df[['name', 'latitude', 'longitude']].copy()
        else:
            self.parking_coords = pd.DataFrame({
                'name': self.parking_df['name'],
                'latitude': [22.15] * len(self.parking_df),
                'longitude': [113.55] * len(self.parking_df)
            })
        
        # Road traffic
        self.road_traffic_df = pd.read_csv(self.config['data']['road_traffic'])
        self.road_traffic_df[['road_lat', 'road_lon']] = self.road_traffic_df['roadCoordinates'].apply(
            lambda x: pd.Series(self._parse_road_coordinates(x))
        )
        road_clean = self.road_traffic_df[self.road_traffic_df['road_lat'].notna()].copy()
        road_clean['traffic'] = road_clean['newTrafficLevel'].fillna(road_clean['trafficLevel'])
        self.road_agg = road_clean.groupby(['road_lat', 'road_lon'])['traffic'].mean().reset_index()
        
        min_r, max_r = self.road_agg['traffic'].min(), self.road_agg['traffic'].max()
        self.road_agg['normalized'] = (self.road_agg['traffic'] - min_r) / (max_r - min_r) if max_r > min_r else 0.5
        
        # Zone traffic
        self.zone_traffic_df = pd.read_csv(self.config['data']['zone_traffic'])
        self.zone_traffic_df[['zone_lat', 'zone_lon']] = self.zone_traffic_df['coordinates'].apply(
            lambda x: pd.Series(self._parse_zone_coordinates(x))
        )
        zone_clean = self.zone_traffic_df[self.zone_traffic_df['zone_lat'].notna()].copy()
        zone_clean['traffic'] = zone_clean['newTrafficLevel'].fillna(zone_clean['trafficLevel'])
        self.zone_agg = zone_clean.groupby(['zone_lat', 'zone_lon'])['traffic'].mean().reset_index()
        
        min_z, max_z = self.zone_agg['traffic'].min(), self.zone_agg['traffic'].max()
        self.zone_agg['normalized'] = (self.zone_agg['traffic'] - min_z) / (max_z - min_z) if max_z > min_z else 0.5
        
        # Bus stops
        bus_stops = []
        bus_dir = self.config['data']['bus_stops_dir']
        json_files = glob.glob(f'{bus_dir}/bus_stations_s_*.json')
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    entity = data.get('entity', data)
                    lat, lon = entity.get('lat'), entity.get('lng')
                    
                    if lat and lon:
                        bus_stops.append({
                            'latitude': float(lat),
                            'longitude': float(lon),
                            'name': str(entity.get('title', '')).strip()
                        })
            except:
                continue
        
        self.bus_stops_df = pd.DataFrame(bus_stops) if bus_stops else pd.DataFrame
