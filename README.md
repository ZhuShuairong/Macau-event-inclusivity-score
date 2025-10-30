# Macau Event Inclusivity Scorer

A RoBERTa and Data-driven tool that analyzes event accessibility and inclusivity using machine learning, spatial analysis, and multi-dimensional scoring.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **ML-Powered Classification**: RoBERTa transformer model predicts event characteristics (cost, complexity, activity level, etc.)
- **Spatial Accessibility Analysis**: Calculates proximity to public transportation, parking, and evaluates traffic conditions
- **Age-Inclusive Scoring**: Determines suitability for youth (18-35), adults (36-64), and seniors (65+)
- **Configurable Weights**: Customize the importance of different accessibility factors
- **Multi-Format Support**: Processes single events or batch JSON files

## Scoring Dimensions

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

## Quick Start

### Installation

Clone repository
git clone https://github.com/yourusername/macau-event-inclusivity-scorer.git
cd macau-event-inclusivity-scorer

Install dependencies
pip install -r requirements.txt

### Usage

**Score a single event:**
python event_scorer.py example_event.json

**With custom configuration:**
python event_scorer.py your_event.json -c custom_config.yaml -o results.json

**Python API:**
from event_scorer import EventInclusivityScorer

scorer = EventInclusivityScorer('config.yaml')

event = {
"id": "123",
"name": "Community Art Workshop",
"shortDesc": "Free art class for all ages",
"location": [{"coordinate": ["113.55", "22.19"]}]
}

result = scorer.score_event(event)
print(f"Inclusivity Score: {result['inclusivity_score_100']:.2f}/100")

## Data Requirements

Place your data files in the following structure:

data/
- parking/carparks_with_category.csv
- traffic/
- - merged_road_traffic.csv
- - merged_zone_traffic.csv
- bus_stops/*.json

**Required columns:**
- `carparks_with_category.csv`: `name`, `category`, (optional: `latitude`, `longitude`)
- `merged_road_traffic.csv`: `roadCoordinates`, `newTrafficLevel`, `trafficLevel`
- `merged_zone_traffic.csv`: `coordinates`, `newTrafficLevel`, `trafficLevel`

## Model Setup

1. Download the pre-trained RoBERTa model (or train your own)
2. Place model files in `models/roberta-base/`:
   - `config.json`
   - `pytorch_model.bin`
   - `tokenizer_config.json`
   - `vocab.json`
3. Add `label_mappings.pkl` to `models/`

**Model Architecture**: RoBERTa-base fine-tuned for multi-label classification (6 categories, 12 total labels)

## Configuration

Edit `config.yaml` to customize:

weights:
cost_accessibility: 0.25 # Increase economic factor
age_diversity: 0.10 # Decrease demographic factor

distance_normalization:
bus_max_km: 3.0 # Expand acceptable bus distance

## Model Comparison

| Model | Best Hamming Loss | Final Accuracy | Training Time (min) |
|-------|-------------------|----------------|---------------------|
| distilbert-base-uncased | 0.2342 | 0.2100 | 0.98 |
| roberta-base | 0.2000 | 0.3300 | 1.82 |
| albert-base-v2 | 0.2250 | 0.2700 | 1.83 |

### Best Model: roberta-base 🏆

- Hamming Loss: 0.2000
- Accuracy: 0.3300

## Final Results for RoBERTa-base

- Best Hamming Loss: 0.2000
- Final Accuracy: 0.3300
- Training time: 1.82 minutes

### Per-Category Performance

| Category | Accuracy |
|----------|----------|
| activity_level | 0.8700 |
| complexity | 0.8700 |
| cost | 0.7300 |
| noise_level | 0.8200 |
| cultural_type | 0.7800 |
| audience_scope | 0.6900 |

## Event Template

Use `event_template.json` to format your events:

{
"id": "unique_id",
"name": "Event Name",
"month": "2025-11",
"shortDesc": "Brief description...",
"location": [{
"name": "Venue Name",
"coordinate": ["longitude", "latitude"]
}]
}

## Output Format

{
"event_id": "12035",
"name": "Art Exhibition",
"inclusivity_score_100": 67.45,
"cost": "cheap_or_free",
"complexity": "simple",
"activity_level": "non_active",
"suitable_for_young": 1,
"suitable_for_adult": 1,
"suitable_for_senior": 1,
"nearest_bus_stop_km": 0.234,
"parking_1_category": "Commercial",
...
}

## Methodology

Based on research in urban accessibility and inclusive design:

1. **Text Analysis**: RoBERTa transformer with AdamW optimizer, 5 epochs, multi-label BCE loss
2. **Spatial Matching**: KDTree nearest-neighbor search with Haversine distance (Earth radius: 6371km)
3. **Age Suitability Rules**:
   - Youth excluded: community + quiet + non_active + cultural (all 4)
   - Senior excluded: ≥2 of (loud, costly, active)
4. **Score Normalization**: Distance-based decay functions, inverted traffic metrics

## Contributing

Contributions welcome! Areas for improvement:
- Real-time traffic API integration
- Additional ML models (ALBERT, DistilBERT comparison)
- Multi-language support (Portuguese, Chinese)
- Web dashboard interface

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Macau Tourism Data: https://www.macaotourism.gov.mo
- DSAT Traffic Data: Macau Transport Bureau
- HuggingFace Transformers library

## Contact

Questions? Open an issue and we aim to respond ASAP!

---

**Note**: This tool provides indicative scores. Actual accessibility may vary. Always verify with event organizers.
