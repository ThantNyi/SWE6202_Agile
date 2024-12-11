import requests
import json

# Base URL of your API
BASE_URL = "http://127.0.0.1:5000/weather"

# 1. Test to Add a New Weather Record (POST request)
def test_add_weather_record():
    payload = {
        "date": "2024-12-11",
        "time": "12:30:00",
        "timezone_offset": "UTC+00:00",
        "coordinates": "40.7128,-74.0060",
        "temperature_water": 18.5,
        "temperature_air": 20.0,
        "humidity": 75.0,
        "wind_speed": 15.5,
        "wind_direction": 90.0,
        "precipitation": 0.0,
        "haze": 10.0,
        "notes": "Clear skies"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)

    if response.status_code == 200:
        print("Weather record added successfully!")
        print("Response:", response.json())
    else:
        print("Failed to add weather record. Status Code:", response.status_code)
        print("Response:", response.text)


# 2. Test to Get All Weather Records (GET request)
def test_get_weather_records():
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        print("Weather records retrieved successfully!")
        print("Response:", json.dumps(response.json(), indent=2))
    else:
        print("Failed to retrieve weather records. Status Code:", response.status_code)
        print("Response:", response.text)


# 3. Test to Get a Single Weather Record by ID (GET request)
def test_get_weather_record_by_id(record_id):
    url = f"{BASE_URL}/{record_id}"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Weather record {record_id} retrieved successfully!")
        print("Response:", response.json())
    else:
        print(f"Failed to retrieve weather record {record_id}. Status Code:", response.status_code)
        print("Response:", response.text)


# 4. Test to Delete a Weather Record by ID (DELETE request)
def test_delete_weather_record(record_id):
    url = f"{BASE_URL}/{record_id}"
    response = requests.delete(url)

    if response.status_code == 200:
        print(f"Weather record {record_id} deleted successfully!")
        print("Response:", response.json())
    else:
        print(f"Failed to delete weather record {record_id}. Status Code:", response.status_code)
        print("Response:", response.text)


# Main function to test the API
if __name__ == "__main__":
    # Test adding a new weather record
    test_add_weather_record()

    # Optionally, you can use the `test_get_weather_records()` to view all records or 
    # `test_get_weather_record_by_id(record_id)` and `test_delete_weather_record(record_id)`
    # with actual IDs after records are added.
