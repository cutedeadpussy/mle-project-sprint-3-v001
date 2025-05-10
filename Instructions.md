# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-project-sprint-3-v001

Так как модель не помещается в репозиторий по размерам, то сначала ее следует скачать и поместить в models/
В программе я использую название файла model.pkl
Поэтому, тот кто будет проверять, пожалуйста после скачивания моей модели из проекта 2, назови ее model.pkl
Вот ссылка на мою последнюю модель из проекта 2: s3://s3-student-mle-20250227-88b3651024/18/8e316e6fdf50422ebdf3a584d7b06857/artifacts/model/model.pkl

## 1. FastAPI микросервис в виртуальном окружение
```python
# команды для создания окружения и установки библиотек
python3.10 -m venv .project3_venv
source .project3_venv/bin/activate
pip install -r services/requirements.txt

# команда перехода в директорию
cd services/

# команда запуска сервиса с помощью uvicorn
uvicorn ml_service.flat_app:app --port 1702 --host 0.0.0.0
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:1702/predict?flat_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "building_type_int_1.0": 0, "building_type_int_2.0": 0, "rooms": 2, "building_id": 21974, "1/floor": 0.2, "building_epoch_2.0": 1, "total_area": 54, "ceiling_height": 2.8, "first_floor_True": 0, "longitude": 37.44, "last_floor_True": 0, "floor": 5, "1/distance_from_center": 0.0665, "housing_type_многоэтажка": 1 }'
```


## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию
cd services/

# Для создания Docker-образа и запуска в контейнере без системы мониторинга
docker build -f Dockerfile_ml_service_с -t ml_service_image .
docker run -d --name ml_service_container -p 1702:1702 ml_service_image

# Также, исходя из изначального шаблона задания, которое возможно ошибочно подразумевает использовать docker compose:
# команда для запуска микросервиса в режиме docker compose
docker compose up --build
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:1702/predict?flat_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "building_type_int_1.0": 0, "building_type_int_2.0": 0, "rooms": 2, "building_id": 21974, "1/floor": 0.2, "building_epoch_2.0": 1, "total_area": 54, "ceiling_height": 2.8, "first_floor_True": 0, "longitude": 37.44, "last_floor_True": 0, "floor": 5, "1/distance_from_center": 0.0665, "housing_type_многоэтажка": 1 }'
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию
cd services/

# команда для запуска микросервиса в режиме docker compose
docker compose up --build
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:1702/predict?flat_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "building_type_int_1.0": 0, "building_type_int_2.0": 0, "rooms": 2, "building_id": 21974, "1/floor": 0.2, "building_epoch_2.0": 1, "total_area": 54, "ceiling_height": 2.8, "first_floor_True": 0, "longitude": 37.44, "last_floor_True": 0, "floor": 5, "1/distance_from_center": 0.0665, "housing_type_многоэтажка": 1 }'
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует 20 запросов в течение 10 секунд, для чистоты эксперимента все величины кроме расположения квартиры берутся случайно

```python
# команды необходимые для запуска скрипта
python test_requests.py
```

Адреса сервисов:
- микросервис: http://localhost:1702
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000