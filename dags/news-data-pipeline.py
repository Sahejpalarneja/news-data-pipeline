import os
from datetime import timedelta
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from scraper.runScraper import runScraper
from cleaner.runCleaner import runCleaner
from database.writeData import writeData



#DAG arguments
dag_arguments = {
    'owner': 'sahejpal arneja',
    'start_date': days_ago(0),
    'email': ['sahejpalarneja@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 2,
    'retry_dalay': timedelta(minutes=5)
}

#DAG Definition
dag = DAG(
    'news-data-pipeline',
    description='News Pipeline DAG',
    default_args=dag_arguments,
    schedule_interval=timedelta(days=1)
)

#Task Definition
scrape_data = PythonOperator(
    task_id='scrape-articles',
    python_callable=runScraper,
    dag=dag
)

clean_data = PythonOperator(
    task_id='clean-data',
    python_callable=runCleaner,
    dag=dag
)

write_data = PythonOperator(
    task_id='write-to-DB',
    python_callable=writeData,
    dag=dag
)

#pieline definition
scrape_data >> clean_data >> write_data