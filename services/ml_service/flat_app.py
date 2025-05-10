"""FastAPI-приложение для предсказания цен на квартиры."""

from fastapi import FastAPI
from ml_service.fast_api_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter, Summary

app = FastAPI()

app.handler = FastApiHandler()
# Инициализируем и запускаем экспортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Метрики
REQUEST_DURATION = Summary(
    'main_app_request_duration_seconds',
    'Time spent processing predict requests'
)

REQUEST_COUNT = Counter(
    'main_app_requests_total',
    'Total count of prediction requests',
    ['status']  # Метка для успешных/неуспешных запросов
)

PREDICTION_PRICE_HISTOGRAM = Histogram(
    'main_app_prediction_price',
    'Histogram of predicted apartment prices',
    buckets=(1_000_000, 5_000_000, 10_000_000, 20_000_000, 50_000_000, 100_000_000)
)

EXPENSIVE_PREDICTIONS_COUNT = Counter(
    'main_app_expensive_predictions_total',
    'Count of predictions where price > 20 million'
)

@app.post("/predict")
@REQUEST_DURATION.time()
def predict(flat_id: str, model_params: dict):
    """Функция для получения предполагаемой стоимости квартиры.

    Args:
        flat_id (str): Идентификатор квартиры.
        model_params (dict): Параметры квартиры, которые нужно передать в модель.

    Returns:
        dict: Предсказание цены квартиры.
    """
    try:
        all_params = {
            "flat_id": flat_id,
            "model_params": model_params
        }

        # Увеличиваем счетчик запросов
        REQUEST_COUNT.labels(status="success").inc()

        prediction = app.handler.handle(all_params)
        price = prediction['price']

        # Записываем цену в гистограмму
        PREDICTION_PRICE_HISTOGRAM.observe(price)

        # Считаем дорогие квартиры (>20M)
        if price > 20_000_000:
            EXPENSIVE_PREDICTIONS_COUNT.inc()

        return {'prediction': prediction}

    except Exception as e:
        # Увеличиваем счетчик неудачных запросов
        REQUEST_COUNT.labels(status="error").inc()
        raise e