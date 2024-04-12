from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.append(os.getcwd())
import weather_1

os.environ['NO_PROXY'] = '*'


with DAG(
    'add_weather3',
    # Параметры по умолчанию для тасок
    default_args={
        # Если прошлые запуски упали, надо ли ждать их успеха
        'depends_on_past': False,
        # Кому писать при провале
        'email': ['a.poluesov@mail.ru'],
        # А писать ли вообще при провале?
        'email_on_failure': True,
        # Писать ли при автоматическом перезапуске по провалу
        'email_on_retry': True,
        # Сколько раз пытаться запустить, далее помечать как failed
        'retries': 1,
        # Сколько ждать между перезапусками
        'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
    },
    # Описание DAG (не тасок, а самого DAG)
    description='add row in csv file',
    # Как часто запускать DAG
    schedule_interval=timedelta(minutes=1),
    # С какой даты начать запускать DAG
    # Каждый DAG "видит" свою "дату запуска"
    # это когда он предположительно должен был
    # запуститься. Не всегда совпадает с датой на вашем компьютере
    start_date=datetime(2024, 1, 1),
    # Запустить за старые даты относительно сегодня
    # https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html
    catchup=False,
    # теги, способ помечать даги
    tags=['AP_projects'],
) as dag:

    t1 = PythonOperator(
        task_id='task1',
        python_callable=weather_1.add_row,
    )

    t1
