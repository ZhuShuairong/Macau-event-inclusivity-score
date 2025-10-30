# Macau Visualization Competition - Data Processing & Visualization

This README documents the data processing pipeline used to generate 10 visualization PNG files for analyzing Macau's transportation and event infrastructure.

---

## Visualizations Generated

1. **Historical Macau Event Locations by Recency.png**
2. **Macau Bus Route Network.png**
3. **Macau Bus Stop Locations by Route Density.png**
4. **Macau Parking Lot Locations by Category.png**
5. **Macau Parking Lot Locations.png**
6. **Macau Traffic Heatmap by Road.png**
7. **Macau Traffic Heatmap by Zone.png**
8. **Macau Visitor Density by District.png**
9. **Macau Visitor Density Choropleth Map.png**
10. **Sample Charts of Mean for each Parking Lot Data.png**

---

## Input Datasets

### 1. **Event Data**
- **Source**: Macau Tourism API (`https://www.macaotourism.gov.mo/api/enf/whatson`)
- **Format**: JSON files (monthly from 2010-2025)
- **Combined File**: `all_macao_events_2020_2025.json`
- **Key Fields**: 
  - Event ID, name, location coordinates
  - Event dates (start/end)
  - Event descriptions and types
  - Venue information with lat/lon

### 2. **Tourist/Visitor Data**
- **Source**: Macau Tourism Bureau DataPlus Portal
- **Format**: Monthly XLSX files (2023-2025)
- **Sheets**: 5 sheets per file
  1. Visitor headcount by time period and district
  2. Visitor arrivals by place of origin
  3. Mainland China arrivals by district
  4. Average length of stay by origin
  5. Mainland China average stay
- **Combined Files**: 5 CSV files (`combined_sheet_1_headcount.csv`, etc.)

### 3. **Geographical Boundary Data**
- **Source**: Kontur Topology Boundaries Dataset
- **File**: `kontur_topology_boundaries_MO_20230628.gpkg`
- **Format**: GeoPackage (vector boundaries)
- **Coverage**: Macau SAR administrative boundaries

### 4. **Bus Stop Data**
- **Source**: DSAT (Transport Bureau) API (`https://dis.dsat.gov.mo:8017`)
- **Format**: JSON files per region (18 regions: s_1 to s_18)
- **Detail Files**: Individual bus stop JSON files with route information
- **Key Fields**: Station ID, code, name, lat/lon, routes served

### 5. **Parking Lot Data**
- **Source**: DSAT Traffic Data
- **File**: `carparks_with_category.csv`
- **Key Fields**: Parking lot ID, name, category (Commercial/Residential/Work), coordinates

### 6. **Traffic Data**
- **Files**: 
  - `merged_road_traffic.csv` - Road-level traffic measurements
  - `merged_zone_traffic.csv` - Zone-level traffic aggregates
- **Key Fields**: Timestamps, location coordinates, normalized traffic intensity

---

## Data Manipulation by Visualization

### **1. Historical Macau Event Locations by Recency.png**

**Data Used**: 
- `all_macao_events_2020_2025.json`
- Geographical boundaries (GPKG)

**Manipulation**:
- Extract event coordinates from nested JSON structure
- Parse event start/end dates to calculate recency
- Assign temporal categories (e.g., recent, past year, historical)
- Create point geometries from lat/lon
- Spatial join with Macau boundaries
- Apply recency-based alpha

**Significance**: 
Shows the spatial distribution of events over time, revealing which districts host more recent vs historical events. Helps identify shifting cultural/activity centers and temporal patterns in event hosting. Areas that have high alpha are more recent and more prominent, may include recent venues built, and low alpha may be locations that are changed.

---

### **2. Macau Bus Route Network.png**

**Data Used**:
- Bus stop JSON files from all 18 regions
- Bus route information from detailed stop data
- Geographical boundaries

**Manipulation**:
- Parse all bus stop JSON files to extract station coordinates
- Extract route information from each station's route list
- Build network graph connecting stops sharing common routes
- Create LineString geometries between connected stops

**Significance**: 
Visualizes the comprehensive public transit network, identifying major transit corridors, route overlaps, and network connectivity. Critical for assessing public transportation accessibility across Macau.

---

### **3. Macau Bus Stop Locations by Route Density.png**

**Data Used**:
- Individual bus stop detail JSON files
- Route count per station

**Manipulation**:
- Load all bus stop JSON files
- Count number of routes serving each station
- Create point geometries from lat/lon
- Normalize route counts to [0,1] scale
- Apply color gradient (yellow to dark red) based on route density

**Significance**: 
Highlights transportation hubs and identifies areas with high vs low transit service. Darker markers indicate major interchange points. Essential for understanding transit accessibility disparities.

---

### **4. Macau Parking Lot Locations by Category.png**

**Data Used**:
- `carparks_with_category.csv`
- Geographical boundaries

**Manipulation**:
- Load parking lot CSV with category labels
- Map Chinese district names to English using translation dictionary
- Create point geometries from coordinates
- Assign categorical colors:
  - Other: Grey
  - Residential: Blue 
  - Work: Red
- Plot with category-based legend

**Significance**: 
Shows spatial distribution of parking facilities by type. Critical for understanding parking accessibility for events and tourism, as it helps predict whether the parking lot will be full at a certain time.

---

### **5. Macau Parking Lot Locations.png**

**Data Used**:
- `carparks.csv` (original without categories)
- Manually geocoded coordinates for 30+ parking lots

**Manipulation**:
- Hardcoded coordinate dictionary for parking lots by ID
- Created DataFrame from parking lot list
- Generated point geometries
- Uniform marker styling (no category differentiation)
- Added statistical text box with total count

**Significance**: 
Provides simple overview of all parking facility locations without categorization. Useful for quickly assessing overall parking infrastructure coverage across Macau's districts. Used to filter out parking lots provided with incorrect longitude and latitude.

---

### **6. Macau Traffic Heatmap by Road.png**

**Data Used**:
- `merged_road_traffic.csv`
- Geographical boundaries

**Manipulation**:
- Load road-level traffic CSV with timestamps
- Aggregate traffic intensity by road segment coordinates
- Compute mean/median traffic values per road
- Normalize traffic intensity to [0,1] scale
- Create heatmap using kernel density estimation on coordinates
- Apply sequential colormap (white → yellow → red)

**Significance**: 
Identifies congested road segments and traffic patterns. Red zones indicate high-traffic corridors, while cooler colors show less congested areas. Essential for understanding vehicular accessibility and potential barriers to event attendance.

---

### **7. Macau Traffic Heatmap by Zone.png**

**Data Used**:
- `merged_zone_traffic.csv`
- Statistical district boundaries

**Manipulation**:
- Load zone-level traffic aggregates
- Group traffic data by spatial zones/districts
- Calculate normalized traffic intensity per zone
- Spatial join with district polygons
- Create choropleth map with zone-level coloring
- Apply diverging colormap for traffic levels

**Significance**: 
Provides district-level traffic overview, showing which neighborhoods experience higher vehicular load. Complements road-level data with aggregated perspective. Useful for macro-level transportation planning.

---

### **8. Macau Visitor Density by District.png**

**Data Used**:
- `cleaned_combined_sheet_2_visitor_arrivals_by_origin.csv`
- District coordinate mapping dictionary
- Geographical boundaries

**Manipulation**:
- Aggregate visitor arrivals by Statistical_District
- Sum total visitors across all time periods and origins
- Extract first occurrence of lat/lon for each district
- Translate Chinese district names to English
- Rank districts by visitor count (1 = highest)
- Normalize visitor counts to [0,1] for marker sizing
- Calculate marker size: `size = 150 + normalized_visitors * 6850`
- Perform K-Means clustering (k=8) on coordinates
- Plot as circles with visitor-based color gradient
- Add numbered labels with top-right legend

**Significance**: 
Reveals spatial concentration of tourism activity. Larger, darker circles indicate major tourist hotspots. The ranking system quickly identifies top destinations. Critical for understanding crowding, infrastructure strain, and event placement optimization.

---

### **9. Macau Visitor Density Choropleth Map.png**

**Data Used**:
- `cleaned_combined_sheet_2_visitor_arrivals_by_origin.csv`
- Polygonized boundary data
- District mapping dictionary

**Manipulation**:
- Polygonize boundary linestrings using `shapely.ops.polygonize()`
- Create district point geometries from aggregated visitor data
- Perform spatial join (`sjoin`) with predicate='contains'
- Aggregate visitors by polygon (handles multiple points per polygon)
- Fill null values (unmatched polygons) with 0
- Calculate polygon areas for density metrics
- Compute visitors per square meter
- Apply sequential colormap (light blue → dark blue)
- Add numbered labels at polygon centroids
- Generate ranked legend with visitor counts (M/K notation)

**Significance**: 
Area-based representation of tourist density, complementing point-based view. Shows which neighborhoods (not just coordinates) attract the most visitors. Polygon fill makes spatial patterns more intuitive. Essential for district-level policy and resource allocation.

---

### **10. Sample Charts of Mean for each Parking Lot Data.png**

**Data Used**:
- `carparks_with_category.csv` (with temporal parking occupancy data)

**Manipulation**:
- Load parking lot time-series data
- Group by parking lot ID
- Calculate mean occupancy/utilization across all timestamps
- Create bar chart or line plot
- Sort by mean occupancy (descending)
- Add value labels on bars
- Apply consistent color scheme

**Significance**: 
Identifies parking lots with consistently high vs low utilization. High-utilization lots indicate popular areas with potential parking scarcity. Low-utilization lots may indicate underserved areas or excess capacity. Informs parking infrastructure optimization and event planning. Also shows that patterns exist in the parking lot occupancy, matching hypothesised values. Used to categorize which parking lots are for residence, and which is for work.

---

## Overall Significance

This integrated dataset and visualization suite enables:

1. **Event Accessibility Analysis**: Combining event locations with transit/parking/traffic data
2. **Infrastructure Gap Identification**: Finding areas with poor transit or parking coverage
3. **Crowding Assessment**: Matching high-visitor districts with infrastructure capacity
4. **Temporal Pattern Detection**: Understanding how events and visitor patterns shift over time
5. **Policy Recommendations**: Data-driven suggestions for transportation and event planning improvements

The visualizations support the development of an **Inclusivity Score** framework that quantifies event accessibility based on:
- Public transit proximity (bus stops within 2km)
- Parking accessibility and type (commercial > work > residential)
- Traffic congestion levels (road and zone)
- Visitor density (crowding factor)
- Combined weighted scoring for comprehensive accessibility assessment

---

## Technical Details

**Geospatial Processing**:
- CRS transformations: EPSG:4326 (WGS84) ↔ EPSG:3857 (Web Mercator)
- Spatial joins using GeoPandas `sjoin` with various predicates
- Haversine distance calculations for nearest-neighbor analysis
- K-Means clustering for spatial pattern detection

**Data Cleaning**:
- Removed redundant multilingual columns (Chinese/Portuguese/English → single English column)
- Standardized column names (removed newlines, special characters)
- Geocoded district names to coordinates using manual mapping dictionary
- Normalized numerical features to [0,1] scale for comparability

**Visualization Libraries**:
- GeoPandas for spatial data handling
- Matplotlib for plotting
- Shapely for geometric operations
- Scikit-learn for clustering and scaling

---

## Dataset Statistics

- **Events**: 1000+ unique events (2010-2025)
- **Bus Stops**: 700+ stations across 18 regions
- **Parking Lots**: 50+ facilities with categorization
- **Districts**: 24 statistical districts with visitor data
- **Temporal Coverage**: Monthly tourist data (2023-2025), historical events (2010-2025)

---

## Notes

- District name translations are handled via hardcoded mapping dictionary
- Some parking lots required manual geocoding due to address ambiguity
- Traffic normalization uses min-max scaling within each dataset
- Visitor density calculations sum across all time periods and origins
