import requests
from datetime import datetime, timedelta
from ..config import OPENAQ_V3_URL, OPENAQ_API_TOKEN, CRAWL_DAYS,LOC_ID
from .logger import get_logger

logger = get_logger("fetch_climate")

def get_pm25_sensor_id(location_data):
    for sensor in location_data.get("sensors", []):
        param = sensor.get("parameter", {})
        if param.get("name") == "pm25":
            return sensor.get("id")
    return None

def fetch_air_quality():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=CRAWL_DAYS)

    headers = {
        "X-API-Key": OPENAQ_API_TOKEN
    }

    #PM25 Sensor-ID GET
    response = requests.get(f"{OPENAQ_V3_URL}/locations/{LOC_ID}", headers=headers)
    response.raise_for_status()
    data = response.json().get("results", [])

    SENSOR_ID = get_pm25_sensor_id(data[0])

    # 측정값 수집
    params={
            "datetime_from": start_date.strftime("%Y-%m-%dT00:00:00Z"),
            "datetime_to": end_date.strftime("%Y-%m-%dT00:00:00Z"),
            "limit": 100,
            "page": 1,
            "sort": "desc"
        }
    all_results = []
    try:
        while True:
            response = requests.get(f"{OPENAQ_V3_URL}/sensors/{SENSOR_ID}/measurements/daily", params=params, headers=headers)
            response.raise_for_status()
            data = response.json().get("results", [])
            all_results.extend(data)

            logger.info(f"Fetched {len(data)} records from page {params['page']}")

            if len(data) < params["limit"]:
                break
            params["page"] += 1

    except Exception as e:
        logger.error(f"Error fetching climate data: {e}")

    return all_results