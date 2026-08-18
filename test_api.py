import requests

data = {
    "skills": "Python, SQL",
    "qualification": "Master's in Data Science",
    "experience_level": "Mid"
}

resp = requests.post("http://localhost:5000/api/predict", json=data)
print(resp.status_code)
print(resp.text)
