from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.append(os.getcwd())
import data
import train
import test_model


file_path = './dataset/iris.csv'
train_path = './dataset/iris_train.csv'
model_path = './model.pkl'
test_path = './dataset/iris_test.csv'


with DAG(
    'logreg',
    # Параметры по умолчанию для тасок
    default_args={
        # Если прошлые запуски упали, надо ли ждать их успеха
        'depends_on_past': False,
        # Кому писать при провале
        'email': ['a.poluesov@mail.ru'],
        # А писать ли вообще при провале?
        'email_on_failure': False,
        # Писать ли при автоматическом перезапуске по провалу
        'email_on_retry': False,
        # Сколько раз пытаться запустить, далее помечать как failed
        'retries': 1,
        # Сколько ждать между перезапусками
        'retry_delay': timedelta(minutes=5),  # timedelta из пакета datetime
    },
    # Описание DAG (не тасок, а самого DAG)
    description='logreg model',
    # Как часто запускать DAG
    schedule_interval=timedelta(days=1),
    # С какой даты начать запускать DAG
    # Каждый DAG "видит" свою "дату запуска"
    # это когда он предположительно должен был
    # запуститься. Не всегда совпадает с датой на вашем компьютере
    start_date=datetime(2022, 1, 1),
    # Запустить за старые даты относительно сегодня
    # https://airflow.apache.org/docs/apache-airflow/stable/dag-run.html
    catchup=False,
    # теги, способ помечать даги
    tags=['example'],
) as dag:

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=data.load_data,
    )

    prepare_data_task = PythonOperator(
        task_id='prepare_data',
        python_callable=data.prepare_data,
        op_kwargs={'csv_path': file_path},
    )

    train_data = PythonOperator(
        task_id='train_data',
        python_callable=train.train,
        op_kwargs={'train_csv': train_path},
    )

    test_data = PythonOperator(
        task_id='test_data',
        python_callable=test_model.test,
        op_kwargs={'model_path': model_path,
                   'test_csv': test_path},
    )

    load_data_task >> prepare_data_task >> train_data >> test_data
