FROM python:3.9-slim

WORKDIR /app
# Installs needed Linux packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential git && \
    apt-get clean -y

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
RUN ls -la

# Install pip requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

CMD ["./start.sh"]
