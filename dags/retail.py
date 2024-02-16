# retail.py
from airflow.decorators import dag, task
from datetime import datetime

from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType

def check_load(scan_name='check_load', checks_subpath='sources'):
    from include.soda.check_function import check
    return check(scan_name, checks_subpath)

def check_transform(scan_name='check_transform', checks_subpath='transform'):
    from include.soda.check_function import check

    return check(scan_name, checks_subpath)

@dag(
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=['retail'],
)
def retail():

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_csv_to_gcs',
        src='include/dataset/online_retail_encoded.csv',
        dst='raw/online_retail.csv',
        bucket='p001_retail',
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail',
        gcp_conn_id='gcp',
    )
    
    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://p001_retail/raw/online_retail.csv',
            conn_id='gcp',
            filetype=FileType.CSV
        ),
        output_table=Table(
            name='raw_invoices',
            conn_id='gcp',
            metadata=Metadata(schema='retail')
        ),
        use_native_support=False,
    )
    
    check_load_task = PythonOperator(
        task_id='check_load',
        python_callable = check_load,
    )
    
    transform = DbtTaskGroup(
        group_id='transform',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/transforms']
        )
    )
    
    check_transform_task = PythonOperator(
        task_id='check_transform',
        python_callable=check_transform,
    )
    
    report = DbtTaskGroup(
        group_id='report',
        project_config=DBT_PROJECT_CONFIG,
        profile_config=DBT_CONFIG,
        render_config=RenderConfig(
            load_method=LoadMode.DBT_LS,
            select=['path:models/report']
        )
    )
retail()