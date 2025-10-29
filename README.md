# Macau Event Inclusivity Scorer 🎯

A RoBERTa and data-powered tool that analyzes event accessibility and inclusivity using machine learning, spatial analysis, and multi-dimensional scoring.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 Features

- **ML-Powered Classification**: RoBERTa transformer model predicts event characteristics (cost, complexity, activity level, etc.)
- **Spatial Accessibility Analysis**: Calculates proximity to public transportation, parking, and evaluates traffic conditions
- **Age-Inclusive Scoring**: Determines suitability for youth (18-35), adults (36-64), and seniors (65+)
- **Configurable Weights**: Customize the importance of different accessibility factors
- **Multi-Format Support**: Processes single events or batch JSON files

## 📊 Scoring Dimensions

The inclusivity score (0-100) is computed from 9 weighted components:

| Component | Weight | Description |
|-----------|--------|-------------|
| Bus Proximity | 8% | Distance to nearest bus stops |
| Parking Proximity | 8% | Distance to nearest parking lots |
| Parking Category | 4% | Type of parking (Commercial > Work > Residential) |
| Traffic Level | 5% | Road and zone congestion (inverted) |
| Visitor Density | 5% | Expected crowding (inverted) |
| Cost Accessibility | 20% | Free/cheap vs. costly events |
| Complexity | 20% | Simple vs. complicated activities |
| Activity Level | 15% | Physical demands (non-active scores higher) |
| Age Diversity | 15% | Suitability across age groups |

## 🚀 Quick Start

### Installation

