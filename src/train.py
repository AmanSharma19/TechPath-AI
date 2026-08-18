import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Load data
df = pd.read_csv("data/candidate_job_role_dataset.csv")

# Process skills
df["skills_list"] = df["skills"].apply(
    lambda x: [skill.strip() for skill in str(x).split(",") if skill.strip()]
)

# Extract features
df["profile"] = df.apply(
    lambda row: (
        tuple(row["skills_list"]),
        row["qualification"],
        row["experience_level"],
    ),
    axis=1,
)

unique_profiles = df["profile"].drop_duplicates().reset_index(drop=True)
train_profiles, test_profiles = train_test_split(unique_profiles, test_size=0.20, random_state=42)

train_mask = df["profile"].isin(train_profiles)

train_skills = df.loc[train_mask, "skills_list"]
mlb = MultiLabelBinarizer()
train_skill_matrix = mlb.fit_transform(train_skills)
skill_df_train = pd.DataFrame(train_skill_matrix, columns=mlb.classes_, index=df.index[train_mask])

# Prepare full dataset (for final training we can use all data to get the best model)
all_skills = df["skills_list"]
all_skill_matrix = mlb.transform(all_skills)
skill_df_all = pd.DataFrame(all_skill_matrix, columns=mlb.classes_, index=df.index)

features_all = pd.concat([skill_df_all, df[["qualification", "experience_level"]]], axis=1)
y_all = df["job_role"]

skill_columns = skill_df_all.columns.tolist()
categorical_columns = ["qualification", "experience_level"]

preprocessor = ColumnTransformer(
    transformers=[
        ("skills", "passthrough", skill_columns),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_columns)
    ]
)

rf_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)

rf_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", rf_model)
])

print("Training model...")
rf_pipeline.fit(features_all, y_all)
print("Model trained!")

os.makedirs("models", exist_ok=True)
joblib.dump(rf_pipeline, "models/rf_model_pipeline.pkl")
joblib.dump(mlb, "models/mlb_encoder.pkl")
print("Model and MLB encoder saved!")
