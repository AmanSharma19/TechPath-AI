from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Load Models
print("Loading models...")
pipeline = joblib.load('models/rf_model_pipeline.pkl')
mlb = joblib.load('models/mlb_encoder.pkl')
skill_columns = list(mlb.classes_)
classes = pipeline.classes_
print("Models loaded successfully.")

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        skills = data.get('skills', "")
        qualification = data.get('qualification', "")
        experience_level = data.get('experience_level', "")

        # Parse skills
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        
        # Transform using MLB
        skill_matrix = mlb.transform([skill_list])
        skill_df = pd.DataFrame(skill_matrix, columns=skill_columns)
        
        # Combine with categorical features
        skill_df['qualification'] = qualification
        skill_df['experience_level'] = experience_level
        
        # Get Probabilities
        proba = pipeline.predict_proba(skill_df)[0]
        
        # Get Top 3
        top_indices = proba.argsort()[-3:][::-1]
        
        top_careers = []
        for i in top_indices:
            top_careers.append({
                "role": classes[i],
                "confidence": round(float(proba[i]) * 100, 2)
            })
            
        return jsonify({"success": True, "predictions": top_careers})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
