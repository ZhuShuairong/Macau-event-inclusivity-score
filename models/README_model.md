# Model Files

## Required Files

Place your trained RoBERTa model here:

models/
├── roberta-base/
│ ├── config.json
│ ├── pytorch_model.bin
│ ├── tokenizer_config.json
│ ├── vocab.json
│ ├── special_tokens_map.json
│ └── tokenizer.json
└── label_mappings.pkl

## Model Specifications

- **Architecture**: RoBERTa-base (12 layers, 768 hidden, 12 attention heads)
- **Parameters**: ~125M
- **Task**: Multi-label classification (6 categories)
- **Training**: 500 labeled events, 5 epochs, AdamW optimizer
- **Performance**: ~85% Hamming accuracy

## Label Categories

{
'activity_level': ['active', 'non_active'],
'complexity': ['simple', 'complicated'],
'cost': ['cheap_or_free', 'costly'],
'noise_level': ['quiet', 'loud'],
'cultural_type': ['cultural', 'non_cultural'],
'audience_scope': ['community', 'international']
}

## Alternative: Download Pre-trained Model

If you don't have a trained model:
1. Use base RoBERTa: `roberta-base` from HuggingFace
2. Fine-tune on your labeled events
3. Save with: `model.save_pretrained('./models/roberta-base')`
