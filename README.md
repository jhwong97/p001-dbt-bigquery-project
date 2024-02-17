# Online Retail Sales Analysis
## Introduction
This personal project is a replication of work from this [Data Engineer Project](https://www.youtube.com/watch?v=DzxtCxi4YaA) with some minor tweaks. It provides good hands-on experiences for the following parts:
- To create a complete ELT data pipeline using Airflow to perform data analysis work.
- To utilise Astro CLI in setting up the Airflow local environment.
- To perform data quality check on data extraction and transformation parts via SODA.
- To integrate dbt into the data pipeline as to automate the data transformation and loading it into data warehouse.
- To upload data to GCS and ingesting the data into BigQuery table using the Astro SDK.

## ELT Pipeline
The ELT pipeline is illustrated below:

![alt text](/images/pipeline.png)

## Steps for Replicating Project Work
### Prerequisites
The followings tools are required for this project:
- Docker (Follow the instructions [here](https://docs.docker.com/desktop/install/windows-install/))
- Astro CLI (Follow the instructions [here](https://docs.astronomer.io/astro/cli/install-cli))
- SODA (Sign Up the 45-days free trial [here](https://www.soda.io/))
- A Google Cloud account

### Obtaining the Datasets
The dataset used for this project is obtained from [Kaggle-Online Retail](https://www.kaggle.com/datasets/tunguz/online-retail). The metadata of the dataset is as below:

| Column | Description |
|---|---|
|InvoiceNo | Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation.|
|StockCode| Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.|
|Description|Product (item) name. Nominal.|
|Quantity|The quantities of each product (item) per transaction. Numeric.|
|InvoiceDate|Invoice Date and time. Numeric, the day and time when each transaction was generated.|
|UnitPrice|Unit price. Numeric, Product price per unit in sterling.|
|CustomerID|Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer.|
|Country|Country name. Nominal, the name of the country where each customer resides.|

Special notes:
- The .csv file from the stated link contains data that are not able to decoded with **UTF-8**. Therefore, it is advised to use pandas to replace the errors and re-save it.
```
df.to_csv(filepath,encoding='UTF-8', encoding_errors='replace')
```
### Initiating the Apache Airflow
With the installation of Astro CLI, run the below command to set up the basic structure of the project which included the essential files and directories needed to get started with **Airflow development**.
```
astro dev init
```

After initiating the files and directories, the directory structure will be as below:
```
.
├── Dockerfile
├── README.md
├── airflow_settings.yaml
├── dags
│   ├── example_dag_advanced.py
│   └── example_dag_basic.py
├── include
├── packages.txt
├── plugins
├── requirements.txt
└── tests
    └── dags
        └── test_dag_example.py
```
**Astro** helps in simplifying the data pipeline development, making it easier to work with **Airflow**.