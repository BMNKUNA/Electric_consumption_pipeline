🔌 Real-time Electricity Consumption Data Pipeline (End-to-End)
This project demonstrates an end-to-end real-time data streaming pipeline for electricity consumption in Gauteng using Python, Kafka, Docker, from local machine to  Google Cloud services. It simulates smart meter data generation, performs real-time validation, and persists clean data from msqlite to into a managed SQL database, ready for analytics.
Note: I have included my local scripts and GCP scrpits inside my VM) I practically workd on the Locally ones and aided adjsutments on deploymnent to VM)

🧠 Project Overview
This pipeline continuously generates and streams synthetic electricity consumption data, which is processed and stored for analytics and visualization.

💡 Architectural Diagram
Here's the architectural overview of the deployed pipeline on Google Cloud
![DE Pipeline updated](https://github.com/user-attachments/assets/117d5037-db4e-4088-8069-20067697913a)


📌 Use Case
Real-time ingestion and validation of electricity consumption metrics.

Scalable and fault-tolerant architecture using Kafka and Docker.

Storage and analysis of clean data in Google Cloud SQL via Cloud Studio.

🚀 Key Components & Technologies
Final Component	Role	Tech Stack (GCP)
Producer	Simulates data (e.g., datagen-producer.py)	Python, Docker
Kafka Broker	Message queue for real-time streaming	Apache Kafka (Bitnami Docker Image)
Processor	Validates and filters incoming data (streamer.py)	Python, Docker
Transporter	Writes valid data to database (google_cloud_writer.py)	Python, psycopg2, Docker
Database	Stores final processed data	Google Cloud SQL (PostgreSQL)
Analytics	Query & visualize using interactive SQL	Cloud SQL + SQL Workspace / Cloud Studio

🔁 Pipeline Flow (Localy development to GCP instance)
Data Generator: datagen-producer.py creates synthetic consumption data (city, sector, voltage, power usage).

Kafka Broker: Manages topics like electric_data_topic and processed_electric_data_topic.

Streamer: streamer.py filters valid data (voltage 200–250V, power ≤ 5000 kWh).

Writer: google_cloud_writer.py writes clean data to Google Cloud SQL.

Analytics: Use SQL Studio or Notebooks for querying, visualization, and modeling.

🛠️ Development Journey
📍 Local Development Phase
Built and tested all Python scripts locally.

Used SQLite for initial development and testing.

Ran Kafka via Docker Compose locally.

Ensured rapid iteration and debugging before incurring cloud costs.

☁️ Cloud Migration Phase
Migrated from SQLite to Google Cloud SQL (PostgreSQL).

Dockerized all components.(toughest aprt of the whole proejct) Interchange network on Kfaka and Docker in compute configuration via VM and clod sql)

Deployed Kafka and Python containers on Google Compute Engine (ARM64 VM).

Configured systemd for service persistence on reboot.

🗃️ Data Schema
Table: gp_electric_cons

Field	Type
id	INT
timestamp	TIMESTAMP
city	TEXT
sector	TEXT
power_cons_in_kwh	FLOAT
voltage	INT

Example query:

sql
Copy
Edit
SELECT * FROM gp_electric_cons;
📊 Example Output (Google Cloud SQL)
id	timestamp	city	sector	power_cons_in_kwh	voltage
1	1.7494794e+09	Benoni	Commercial	385.76	240
2	1.7494794e+09	Benoni	Industrial	879.46	220
3	1.7494794e+09	Johannesburg	Residential	540.14	220

📉 Analytics with SQL Studio
Time-series trends (daily/weekly consumption)

Sectoral comparisons (residential vs. industrial)

City-level usage heatmaps

Predictive modeling and anomaly detection

🧱 Challenges Faced
🐳 Docker Compatibility Issues
Kafka Bitnami containers were initially incompatible with ARM64 architecture (local M1 MacBook & GCP VM).

Needed to customize Dockerfiles and switch base images to support ARM64.

🔄 Cloud VM Setup
Setting up persistent Docker containers with systemd required:

Custom unit files

Ensuring logs were stored correctly

Auto-starting services on VM reboot

🔐 PostgreSQL Access
Configuring SSL and IAM bindings for Cloud SQL PostgreSQL access from custom Python clients was non-trivial.

Implemented retry logic and connection pooling using psycopg2.

📦 How to Run Locally (Dev Mode)
Clone the repo.

Install Docker and Docker Compose.

Run Kafka and all containers:

bash
Copy
Edit
docker-compose up --build
Open SQL client to inspect SQLite or switch to PostgreSQL setup.

📡 Deployment on Google Cloud
Create a Compute Engine VM (ARM64).

Install Docker and Docker Compose.

Upload project files.

Set up systemd services for each Python container.

Connect Cloud SQL to your Python writer using public IP or private VPC.

📂 Folder Structure
bash
Copy
Edit
.
├── datagen-producer.py
├── streamer.py
├── google_cloud_writer.py
├── docker-compose.yml
├── Dockerfile.producer
├── Dockerfile.streamer
├── Dockerfile.writer
├── requirements.txt
├── README.md
└── diagrams/
    └── DE Pipeline updated.jpg
🧠 Future Enhancements
Integrate monitoring with Prometheus + Grafana.(Learning curve)

Support batch inserts or BigQuery sink. (so familiar with)

Expand sectors and cities for richer simulation.

Add authentication and access control for Cloud SQL. (AIM roles)

📬 Contact
For questions or collaboration, please reach out to me via contact@mondenkuna.co.za or visit https://mondenkuna.co.za

Let me know if you'd like this exported as a README.md file or want a downloadable version!
