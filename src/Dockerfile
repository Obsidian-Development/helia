
    FROM python:latest

    WORKDIR ./app

    COPY . .
    RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

    VOLUME ./app/db

    CMD ["python3", "./main.py"]
