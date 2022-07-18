
# Organization of the project

1. Within the airflow dags folder create a subfolder named `weather_etl`. 
2. In it create an empty file named `__init__.py`.
3. Move all project files to the `weather_etl`.
4. Change all statements importing from `weathers` package to import from `weather_etl.weathers`.
5. Move data folder `data` with all its subfolders to the airflow root and rename it to `weather_data`.
