
"""Класс FastApiHandler, который обрабатывает запросы API."""

import joblib
import pandas as pd

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {
            "flat_id": str,
            "model_params": dict
        }

        self.model_path = "models/model.pkl"
        self.load_churn_model(model_path=self.model_path)
        
        # необходимые параметры для предсказаний цены на квартиру
        self.required_model_params = ['building_type_int_1.0', 'building_type_int_2.0', 'rooms', 'building_id',
                    '1/floor', 'building_epoch_2.0', 'total_area', 'ceiling_height',
                    'first_floor_True', 'longitude', 'last_floor_True', 'floor',
                    '1/distance_from_center', 'housing_type_многоэтажка']

    def load_churn_model(self, model_path: str):
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def price_predict(self, model_params: dict) -> float:
        
        param_df = pd.DataFrame([model_params])
        print(param_df, '\n\n\n')
        print(self.model.predict(param_df))
        return self.model.predict(param_df)[0]
        
    def check_required_query_params(self, query_params: dict) -> bool:
        if "flat_id" not in query_params or "model_params" not in query_params:
            return False
        
        if not isinstance(query_params["flat_id"], self.param_types["flat_id"]):
            return False
                
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        return True
    
    def check_required_model_params(self, model_params: dict) -> bool:

        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    
    def validate_params(self, params: dict) -> bool:
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
        
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
        
    def handle(self, params):
        try:
        # валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                flat_id = params["flat_id"]
                print(f"Predicting for flat_id: {flat_id} and model_params:\n{model_params}")
                # получаем предсказания модели
                predicted_price = self.price_predict(model_params)
                response = {
                    "flat_id": flat_id, 
                    "price": predicted_price
                }
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            print(response)
            return response