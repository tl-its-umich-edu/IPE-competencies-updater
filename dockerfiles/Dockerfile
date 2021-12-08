FROM python:3.9-slim

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
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["./start.sh"]
