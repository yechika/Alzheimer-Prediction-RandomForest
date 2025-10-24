---
title: Alzheimer Prediction API
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# Alzheimer Disease Prediction API

Backend API untuk prediksi penyakit Alzheimer menggunakan Random Forest Classifier.

## Model Information

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 93.95%
- **Precision**: 93.97%
- **Recall**: 93.95%
- **Training Data**: 1,719 samples
- **Test Data**: 430 samples

## API Endpoints

### GET /
API information and available endpoints

### GET /health
Health check endpoint

### POST /predict
Predict Alzheimer disease with patient data (JSON body required)

### GET /predict-sample
Get prediction using sample data

## Usage Example

```bash
curl -X POST https://your-space-name.hf.space/predict \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Server will run on `http://127.0.0.1:5000`
