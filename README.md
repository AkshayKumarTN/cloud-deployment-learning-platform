\# DeployHub - Learn Cloud Deployment



🚀 A comprehensive web application that teaches cloud deployment strategies across AWS, Digital Ocean, Docker, and CI/CD pipelines.



\## Features



\- ☁️ \*\*AWS Deployment Guide\*\* - Step-by-step AWS EC2 deployment

\- 💧 \*\*Digital Ocean Guide\*\* - Simple droplet-based deployment

\- 🐳 \*\*Docker Tutorial\*\* - Containerization best practices

\- ⚙️ \*\*CI/CD Pipeline\*\* - Automated deployment with GitHub Actions

\- 📊 \*\*Monitoring\*\* - Prometheus + Grafana integration

\- 🧪 \*\*Live API Demo\*\* - Interactive calculator API



\## Quick Start



\### Prerequisites



\- Python 3.11+

\- Docker and Docker Compose

\- Git



\### Local Development

```bash

\# Clone repository

git clone https://github.com/YOUR\_USERNAME/devops-pipeline-project.git

cd devops-pipeline-project



\# Install dependencies

pip install -r requirements.txt



\# Run application

python src/app.py

```



Visit http://localhost:5000



\### Run Tests

```bash

pip install pytest pytest-cov

pytest tests/ -v --cov=src

```



\### Docker Deployment

```bash

docker-compose up -d

```



Access:

\- \*\*Application:\*\* http://localhost:80

\- \*\*Prometheus:\*\* http://localhost:9090

\- \*\*Grafana:\*\* http://localhost:3000 (admin/admin123)



\## API Documentation



\### POST /api/calculate



Calculate sum of two numbers.



\*\*Request:\*\*

```json

{

&nbsp; "a": 5,

&nbsp; "b": 7

}

```



\*\*Response:\*\*

```json

{

&nbsp; "result": 12,

&nbsp; "operation": "5 + 7"

}

```



\### GET /health



Health check endpoint.



\### GET /metrics



Prometheus metrics endpoint.



\## Architecture

```

┌─────────────┐     ┌──────────────┐     ┌─────────────────┐

│   GitHub    │────▶│ GitHub       │────▶│ Digital Ocean   │

│ Repository  │     │ Actions      │     │ Droplet         │

└─────────────┘     └──────────────┘     └─────────────────┘

&nbsp;                          │

&nbsp;                          ▼

&nbsp;                   ┌──────────────┐

&nbsp;                   │ Docker       │

&nbsp;                   │ Registry     │

&nbsp;                   └──────────────┘

```



\## CI/CD Pipeline



1\. \*\*Test\*\* - Run pytest with coverage

2\. \*\*Build\*\* - Create Docker image

3\. \*\*Push\*\* - Push to GitHub Container Registry

4\. \*\*Deploy\*\* - SSH to server and update containers

5\. \*\*Release\*\* - Create versioned release with artifacts



\## Monitoring



\- \*\*Prometheus\*\* collects metrics from application

\- \*\*Grafana\*\* visualizes metrics with dashboards

\- \*\*Node Exporter\*\* provides system metrics

\- \*\*cAdvisor\*\* monitors container performance



\## Project Structure

```

devops-pipeline-project/

├── src/

│   └── app.py              # Main Flask application

├── tests/

│   └── test\_app.py         # Test suite

├── .github/

│   └── workflows/

│       └── ci-cd.yml       # GitHub Actions workflow

├── Dockerfile              # Docker image definition

├── docker-compose.yml      # Multi-container setup

├── prometheus.yml          # Prometheus configuration

├── requirements.txt        # Python dependencies

└── README.md              # This file

```



\## Environment Variables



Set these in GitHub Secrets:



\- `DO\_HOST` - Digital Ocean droplet IP

\- `DO\_USERNAME` - SSH username (devops)

\- `DO\_SSH\_KEY` - Private SSH key for deployment



\## License



MIT License



\## Author



DevOps Learning Project

 
 
 
