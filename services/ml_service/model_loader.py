import joblib

def load_churn_model(model_path: str):
    try:
        model = joblib.load(model_path)

        print("Model loaded successfully")
    except Exception as e:
        print(f"Failed to load model: {e}")
    return model

if __name__ == "__main__":
    model = load_churn_model(model_path='models/project_2_final_model.pkl')
    print(f'Model parameter names: {model.feature_names_in_}')