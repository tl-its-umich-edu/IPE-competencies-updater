FROM python:3.8-slim

# Installs needed Linux packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential git netcat && \
    apt-get clean -y

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["./start.sh"]
