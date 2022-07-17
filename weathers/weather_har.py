from weathers import weather_fio as fio
from datetime import datetime


def transform_json_data(data):
    dates = []
    temps = []
    pressures = []
    pops = []
    precip = []
    #precipitations = []
    for hour in data["hourly"]:
        dates.append(datetime.utcfromtimestamp(hour["dt"]).strftime('%Y-%m-%dT%H:%M:%S%z'))
        temps.append(hour["temp"])
        pressures.append(hour["pressure"])
        pops.append(round(hour["pop"] * 100, 1))            # Probabilities of precipitation
        if "rain" in hour:
            precip.append(hour["rain"]["1h"])
        elif "snow" in hour:
            precip.append(hour["snow"]["1h"])
        else:
            precip.append(0)
    #print(type(raw_data["hourly"]))
    d_len = len(data["hourly"])
    result = {
        "city_name": [data["city"]] * d_len,
        "country": [data["country"]] * d_len,
        "city_lat": [data["city_lat"]] * d_len,
        "city_lon": [data["city_lon"]] * d_len,
        "geo_lat": [data["lat"]] * d_len,
        "geo_lon": [data["lon"]] * d_len,
        "timezone": [data["timezone"]] * d_len,
        "retrieved": [datetime.utcfromtimestamp(data["current"]["dt"]).strftime('%Y-%m-%dT%H:%M:%S%z')] * d_len,
        "forecast_dt": dates,
        "temperature": temps,
        "air_pressure": pressures,
        "precipitation": precip,
        "probability_of_precipitation": pops
        }
    return result


def run(read_dir, save_dir):
    raw = fio.read_json_file(read_dir)
    harmonized = transform_json_data(raw)
    fio.save_json_file(harmonized, save_dir)
