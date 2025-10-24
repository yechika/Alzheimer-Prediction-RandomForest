# Alzheimer Disease Prediction API

Backend Flask API untuk memprediksi penyakit Alzheimer menggunakan Machine Learning.

## Cara Menjalankan

### 1. Install Dependencies
```bash
pip install flask pandas numpy scikit-learn
```

### 2. Jalankan Server
```bash
python app.py
```

Server akan berjalan di: `http://127.0.0.1:5000`

---

## API Endpoints

### 1. **GET /** - API Information
Mendapatkan informasi tentang API dan daftar endpoint yang tersedia.

**Request:**
```
GET http://127.0.0.1:5000/
```

**Response:**
```json
{
    "message": "Alzheimer Disease Prediction API",
    "version": "1.0",
    "endpoints": {
        "/": "GET - API information",
        "/predict": "POST - Predict Alzheimer disease (with JSON body)",
        "/predict-sample": "GET - Get prediction using sample data",
        "/health": "GET - Health check"
    }
}
```

---

### 2. **GET /health** - Health Check
Memeriksa status kesehatan API dan apakah model sudah dimuat.

**Request:**
```
GET http://127.0.0.1:5000/health
```

**Response:**
```json
{
    "status": "healthy",
    "model_loaded": true,
    "scaler_loaded": true
}
```

---

### 3. **POST /predict** - Predict dengan JSON Body
Melakukan prediksi Alzheimer berdasarkan data pasien yang dikirim via JSON body.

**Request:**
```
POST http://127.0.0.1:5000/predict
Content-Type: application/json
```

**Request Body:**
```json
{
  "Age": 65,
  "Gender": 1,
  "Ethnicity": 2,
  "EducationLevel": 3,
  "BMI": 24.5,
  "Smoking": 0,
  "AlcoholConsumption": 5.0,
  "PhysicalActivity": 8.0,
  "DietQuality": 7.5,
  "SleepQuality": 8.0,
  "FamilyHistoryAlzheimers": 0,
  "CardiovascularDisease": 0,
  "Diabetes": 0,
  "Depression": 0,
  "HeadInjury": 0,
  "Hypertension": 0,
  "SystolicBP": 120,
  "DiastolicBP": 80,
  "CholesterolTotal": 180.0,
  "CholesterolLDL": 100.0,
  "CholesterolHDL": 60.0,
  "CholesterolTriglycerides": 120.0,
  "MMSE": 28.0,
  "FunctionalAssessment": 9.0,
  "MemoryComplaints": 0,
  "BehavioralProblems": 0,
  "ADL": 1.0,
  "Confusion": 0,
  "Disorientation": 0,
  "PersonalityChanges": 0,
  "DifficultyCompletingTasks": 0,
  "Forgetfulness": 0
}
```

**Required Fields (32 total):**
- Age
- Gender
- Ethnicity
- EducationLevel
- BMI
- Smoking
- AlcoholConsumption
- PhysicalActivity
- DietQuality
- SleepQuality
- FamilyHistoryAlzheimers
- CardiovascularDisease
- Diabetes
- Depression
- HeadInjury
- Hypertension
- SystolicBP
- DiastolicBP
- CholesterolTotal
- CholesterolLDL
- CholesterolHDL
- CholesterolTriglycerides
- MMSE
- FunctionalAssessment
- MemoryComplaints
- BehavioralProblems
- ADL
- Confusion
- Disorientation
- PersonalityChanges
- DifficultyCompletingTasks
- Forgetfulness

**Response (Success):**
```json
{
    "success": true,
    "prediction": {
        "diagnosis": "Tidak Alzheimer",
        "class": 0,
        "probability": {
            "tidak_alzheimer": 93.08,
            "alzheimer": 6.92
        }
    },
    "input_data": {
        "Age": "75",
        "Gender": "1",
        ...
    }
}
```

**Response (Error - Missing Fields):**
```json
{
    "error": "Missing required fields",
    "missing_fields": ["Age", "Gender"],
    "required_fields": [...]
}
```

---

### 4. **GET /predict-sample** - Predict dengan Sample Data
Melakukan prediksi menggunakan 2 data pasien sample (sehat & berisiko tinggi).

**Request:**
```
GET http://127.0.0.1:5000/predict-sample
```

**Response:**
```json
{
    "success": true,
    "total_samples": 2,
    "predictions": [
        {
            "patient_id": 1,
            "patient_profile": "Sehat (Risiko Rendah)",
            "diagnosis": "Tidak Alzheimer",
            "class": 0,
            "probability": {
                "tidak_alzheimer": 93.08,
                "alzheimer": 6.92
            },
            "input_data": {
                "Age": 65,
                "Gender": 1,
                "BMI": 24.5,
                ...
            }
        },
        {
            "patient_id": 2,
            "patient_profile": "Berisiko Tinggi",
            "diagnosis": "Alzheimer",
            "class": 1,
            "probability": {
                "tidak_alzheimer": 22.16,
                "alzheimer": 77.84
            },
            "input_data": {
                "Age": 85,
                "Gender": 0,
                "BMI": 19.2,
                ...
            }
        }
    ]
}
```

---

## Testing API

### Menggunakan Browser:
1. Buka browser dan akses:
   - `http://127.0.0.1:5000/` - Info API
   - `http://127.0.0.1:5000/health` - Health check
   - `http://127.0.0.1:5000/predict-sample` - Sample prediction

### Menggunakan PowerShell:
```powershell
# Health check
Invoke-WebRequest -Uri "http://127.0.0.1:5000/health" | Select-Object -Expand Content

# Sample prediction
Invoke-WebRequest -Uri "http://127.0.0.1:5000/predict-sample" | Select-Object -Expand Content

# Predict dengan JSON body - Pasien Sehat
$body = Get-Content "sample_request.json" -Raw
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" -Method POST -Body $body -ContentType "application/json"

# Predict dengan JSON body - Pasien Berisiko Tinggi
$body = Get-Content "sample_request_risiko_tinggi.json" -Raw
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" -Method POST -Body $body -ContentType "application/json"
```

### Menggunakan curl:
```bash
# Health check
curl http://127.0.0.1:5000/health

# Sample prediction
curl http://127.0.0.1:5000/predict-sample

# Predict dengan JSON body - Pasien Sehat
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @sample_request.json

# Predict dengan JSON body - Pasien Berisiko Tinggi
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @sample_request_risiko_tinggi.json
```

---

## Model Information

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 93.95%
- **Precision**: 93.97%
- **Recall**: 93.95%
- **Training Data**: 1,719 samples
- **Test Data**: 430 samples

### Most Important Features:
1. **FunctionalAssessment** (19.45%)
2. **ADL** (18.71%)
3. **MMSE** (12.25%)

---

## File Structure
```
PROJECT/
├── app.py                              # Flask API
├── alzheimer_model.pkl                 # Trained model
├── alzheimer_scaler.pkl                # Data scaler
├── alzheimers_disease_data.csv         # Dataset
├── main.ipynb                          # Jupyter notebook
├── sample_request.json                 # Sample request - Pasien Sehat
├── sample_request_risiko_tinggi.json   # Sample request - Pasien Berisiko
```

---

## Notes

1. Pastikan file `alzheimer_model.pkl` dan `alzheimer_scaler.pkl` ada di folder yang sama dengan `app.py`
2. Semua 32 field harus diisi untuk endpoint `/predict`
3. Gunakan endpoint `/predict-sample` untuk testing cepat
4. API menggunakan POST method dengan JSON body untuk endpoint `/predict`
5. File sample request tersedia: `sample_request.json` dan `sample_request_risiko_tinggi.json`

---

## Response Codes

- **200**: Success
- **400**: Bad Request (missing/invalid parameters)
- **500**: Internal Server Error

---

