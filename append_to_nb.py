import json

with open('notebooks/01_data_cleaning_eda.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "import joblib\n",
        "import os\n",
        "\n",
        "os.makedirs('../models', exist_ok=True)\n",
        "# Random Forest happens to be one of the best performing models, let's save the pipeline\n",
        "joblib.dump(rf_pipeline, '../models/rf_model_pipeline.pkl')\n",
        "print('Model saved to ../models/rf_model_pipeline.pkl')"
    ]
}

nb['cells'].append(new_code_cell)

with open('notebooks/01_data_cleaning_eda.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
