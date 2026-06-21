"""fetch_live_data.py
-------------------
OPTIONAL script to refresh the bundled data from the public live feed.
"""
import os
import requests
import pandas as pd
from pathlib import Path

# Вычисляем путь к проекту (этот файл лежит в <root>/scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "alerts_sample.csv"

def fetch_data():
    url = "https://raw.githubusercontent.com/Vadimkin/ukrainian-air-raid-sirens-dataset/main/datasets/official_data_en.csv"
    print(f"Downloading latest data from: {url}")
    
    # Скачиваем файл
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download data. Status code: {response.status_code}")
        
    # Создаем папку, если её нет
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Сохраняем временный файл, чтобы прочитать его через pandas для проверки
    temp_path = RAW_DATA_PATH.with_suffix('.tmp')
    with open(temp_path, 'wb') as f:
        f.write(response.content)
        
    df = pd.read_csv(temp_path)
    print(f"Downloaded {len(df):,} total rows (all alert levels).")
    
    # Базовая очистка дубликатов
    df = df.drop_duplicates()
    print(f"Deduplicated to {len(df):,} unique alert events.")
    
    # Переименовываем в финальный файл
    if RAW_DATA_PATH.exists():
        os.remove(RAW_DATA_PATH)
    os.rename(temp_path, RAW_DATA_PATH)
    print(f"Updated: {RAW_DATA_PATH}")
    print("You can now run: py -m src.main")

if __name__ == "__main__":
    try:
        fetch_data()
    except Exception as e:
        print(f"Error fetching data: {e}")