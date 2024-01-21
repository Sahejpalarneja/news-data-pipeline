# news-data-pipeline

## Description
- The chat bot will be accessible through he Telegram messaging services
- The users can add the chat bot as one of the chats/conversations and to the services
- The user will have a set of commands that can be used together or separately to get news updates
	- Like . Get the news about sports from 12/01/2024
	- Headlines of of world politics
	- Source of a particular headline
- Each request will trigger the response from the service.
- The data will be refreshed everyday to get the latest data

## Tech Stack

- **Python**
	- For web scraping and data lineage
- **Apache Airflow**
	- For work flow management
	- Has the same  objective as Jenkins but a lot more better for handling Data pipelines
		- You can find a better comparison here: https://stackshare.io/stackups/airflow-vs-jenkins
- **Docker**
	- We use the docker image for airflow , this will be deployed on Azure
- **Azure Container Instances (ACI)**
	- Deploying docker image for the airflow scheduler
- **Azure Database for PostgreSQL servers**
	- Storage for the scraped data
- **Apache Spark**
	- To execute the python scripts
- **Grafana** 
	- For monitoring and KPI visualization
- **Django**
	- Creating the API for the Telegram bot to interact with
- **Azure App Service**
	- Deploying Django API

## Infrastructure

### Data Ingest Pipeline
![Ingest Pipeline](/img/Data_Ingest_Pipeline.jpg)

The above diagram shows the pattern on how the infrastructure is set up for the data pipeline to be ingested data into the DB
1. Apache Airflow manages the workflow and has the scheduler 
2. Airflow triggers Spark jobs to scrape web data using python scripts
	1. Data lineage is also scheduled by Airflow after the scraping is complete
3. Data is then stored inside the PostgreSQL DB in a properly formatted , labelled and annotated manner

### Data output Pipeline
![Output Pipeline](/img/Data_Output_Pipeline.jpg)

The bot works with the help of a Django REST API
- The telegram bot is connected to the Django API by webhooks
- It sends the information to the Azure server through the API requests 
- The Django API queried data from the PostgreSQL DB on Azure and returns the data it in a structured for via message on telegram


### Airflow workflow description
![Alt text](/img/image.png)