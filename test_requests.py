import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:1702/predict"
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

def generate_random_data(flat_id):
    building_type = random.choice([(1, 0), (0, 1), (0, 0)])
    
    return {
        "building_type_int_1.0": building_type[0],
        "building_type_int_2.0": building_type[1],
        "rooms": random.randint(1, 20),
        "building_id": random.randint(1, 20000),
        "1/floor": round(random.uniform(0, 1), 2),
        "building_epoch_2.0": random.randint(0, 1),
        "total_area": random.randint(10, 1000),
        "ceiling_height": round(random.uniform(2, 5), 1),
        "first_floor_True": random.randint(0, 1),
        "longitude": 37.44,
        "last_floor_True": random.randint(0, 1),
        "floor": random.randint(1, 100),
        "1/distance_from_center": 0.0665,
        "housing_type_многоэтажка": random.randint(0, 1)
    }

def send_request(flat_id):
    data = generate_random_data(flat_id)
    params = {"flat_id": flat_id}
    
    try:
        response = requests.post(
            BASE_URL,
            params=params,
            headers=HEADERS,
            json=data,
            timeout=5
        )
        print(f"Request {flat_id}: Status {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Request {flat_id} failed: {str(e)}")

def main():
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for flat_id in range(1, 21):
            executor.submit(send_request, flat_id)
            time.sleep(0.5)
    
    end_time = time.time()
    print(f"All requests completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()