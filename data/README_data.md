# Data Files Guide

## Required Data Files

Place your data files in this directory structure:

### 1. Parking Data
**File**: `parking/carparks_with_category.csv`

Required columns:
- `name`: Parking lot name (Chinese)
- `category`: Commercial, Work, or Residential
- `latitude`: (optional) Decimal degrees
- `longitude`: (optional) Decimal degrees

### 2. Traffic Data
**Files**: 
- `traffic/merged_road_traffic.csv`
- `traffic/merged_zone_traffic.csv`

Required columns for road traffic:
- `roadCoordinates`: Semicolon-separated "lon,lat" pairs
- `newTrafficLevel`: Traffic intensity (1-5)
- `trafficLevel`: Fallback traffic level

Required columns for zone traffic:
- `coordinates`: Semicolon-separated polygon coordinates
- `newTrafficLevel`: Zone traffic intensity

### 3. Bus Stop Data
**Directory**: `bus_stops/`

JSON files with format:
{
"entity": {
"id": "...",
"title": "...",
"lat": "22.xxx",
"lng": "113.xxx",
"routes": [...]
}
}

## Data Sources

- Macau Tourism: https://dataplus.macaotourism.gov.mo/
- DSAT Open Data: https://www.dsat.gov.mo/
