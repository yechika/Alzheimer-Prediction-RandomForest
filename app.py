from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Load model and scaler
print("Loading model and scaler...")
try:
    with open('alzheimer_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('alzheimer_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("Model and scaler loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    scaler = None


@app.route('/', methods=['GET'])
def home():
    """
    Endpoint untuk informasi API
    """
    return jsonify({
        'message': 'Alzheimer Disease Prediction API',
        'version': '1.0',
        'endpoints': {
            '/': 'GET - API information',
            '/predict': 'POST - Predict Alzheimer disease (with JSON body)',
            '/predict-sample': 'GET - Get prediction using sample data',
            '/health': 'GET - Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health():
    """
    Endpoint untuk health check
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint untuk prediksi Alzheimer berdasarkan JSON body
    
    Contoh penggunaan:
    POST /predict
    Content-Type: application/json
    Body: {"Age": 75, "Gender": 1, "Ethnicity": 0, ...}
    """
    try:
        # Ambil data dari JSON body
        data_json = request.get_json()
        
        if not data_json:
            return jsonify({
                'error': 'No JSON data provided',
                'message': 'Please send JSON data in request body'
            }), 400
        
        required_features = [
            'Age', 'Gender', 'Ethnicity', 'EducationLevel', 'BMI', 'Smoking',
            'AlcoholConsumption', 'PhysicalActivity', 'DietQuality', 'SleepQuality',
            'FamilyHistoryAlzheimers', 'CardiovascularDisease', 'Diabetes', 'Depression',
            'HeadInjury', 'Hypertension', 'SystolicBP', 'DiastolicBP',
            'CholesterolTotal', 'CholesterolLDL', 'CholesterolHDL', 'CholesterolTriglycerides',
            'MMSE', 'FunctionalAssessment', 'MemoryComplaints', 'BehavioralProblems',
            'ADL', 'Confusion', 'Disorientation', 'PersonalityChanges',
            'DifficultyCompletingTasks', 'Forgetfulness'
        ]
        
        # Validasi: cek apakah semua field ada
        missing_params = [f for f in required_features if f not in data_json]
        if missing_params:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_params,
                'required_fields': required_features
            }), 400
        
        # Buat dataframe dari JSON data
        data = pd.DataFrame({feature: [float(data_json[feature])] for feature in required_features})
        
        data_scaled = scaler.transform(data)
        
        prediction = model.predict(data_scaled)[0]
        prediction_proba = model.predict_proba(data_scaled)[0]
        
        return jsonify({
            'success': True,
            'prediction': {
                'diagnosis': 'Alzheimer' if prediction == 1 else 'Tidak Alzheimer',
                'class': int(prediction),
                'probability': {
                    'tidak_alzheimer': round(float(prediction_proba[0]) * 100, 2),
                    'alzheimer': round(float(prediction_proba[1]) * 100, 2)
                }
            },
            'input_data': data_json
        })
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid field value',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@app.route('/predict-sample', methods=['GET'])
def predict_sample():
    """
    Endpoint untuk prediksi menggunakan sample data
    Mengembalikan prediksi untuk 2 pasien sample (sehat & berisiko)
    """
    try:
        sample_data = pd.DataFrame({
            'Age': [65, 85],
            'Gender': [1, 0],
            'Ethnicity': [2, 1],
            'EducationLevel': [3, 0],
            'BMI': [24.5, 19.2],
            'Smoking': [0, 1],
            'AlcoholConsumption': [5.0, 18.5],
            'PhysicalActivity': [8.0, 2.0],
            'DietQuality': [7.5, 1.2],
            'SleepQuality': [8.0, 4.5],
            'FamilyHistoryAlzheimers': [0, 1],
            'CardiovascularDisease': [0, 1],
            'Diabetes': [0, 1],
            'Depression': [0, 1],
            'HeadInjury': [0, 1],
            'Hypertension': [0, 1],
            'SystolicBP': [120, 165],
            'DiastolicBP': [80, 95],
            'CholesterolTotal': [180.0, 280.0],
            'CholesterolLDL': [100.0, 190.0],
            'CholesterolHDL': [60.0, 30.0],
            'CholesterolTriglycerides': [120.0, 340.0],
            'MMSE': [28.0, 5.0],
            'FunctionalAssessment': [9.0, 1.5],
            'MemoryComplaints': [0, 1],
            'BehavioralProblems': [0, 1],
            'ADL': [1.0, 8.5],
            'Confusion': [0, 1],
            'Disorientation': [0, 1],
            'PersonalityChanges': [0, 1],
            'DifficultyCompletingTasks': [0, 1],
            'Forgetfulness': [0, 1]
        })
        
        sample_data_scaled = scaler.transform(sample_data)
        
        predictions = model.predict(sample_data_scaled)
        prediction_proba = model.predict_proba(sample_data_scaled)
        
        results = []
        for i in range(len(sample_data)):
            results.append({
                'patient_id': i + 1,
                'patient_profile': 'Sehat (Risiko Rendah)' if i == 0 else 'Berisiko Tinggi',
                'diagnosis': 'Alzheimer' if predictions[i] == 1 else 'Tidak Alzheimer',
                'class': int(predictions[i]),
                'probability': {
                    'tidak_alzheimer': round(float(prediction_proba[i][0]) * 100, 2),
                    'alzheimer': round(float(prediction_proba[i][1]) * 100, 2)
                },
                'input_data': sample_data.iloc[i].to_dict()
            })
        
        return jsonify({
            'success': True,
            'total_samples': len(results),
            'predictions': results
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    
    print("\n" + "="*70)
    print("ALZHEIMER PREDICTION API")
    print("="*70)
    print(f"Server running on: http://0.0.0.0:{port}")
    print("\nAvailable endpoints:")
    print("  GET  /                 - API information")
    print("  GET  /health           - Health check")
    print("  POST /predict          - Predict with JSON body")
    print("  GET  /predict-sample   - Predict with sample data")
    print("="*70 + "\n")
    
    # Use debug=False for production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
