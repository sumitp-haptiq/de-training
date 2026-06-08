FROM python:3.11-slim

# Install system deps
RUN apt-get update && apt-get install -y git curl build-essential libpq-dev

# Install DBT and Postgres adapter
RUN pip install --no-cache-dir dbt-postgres

# Create workspace
WORKDIR /usr/app
COPY . .

CMD ["bash"]
