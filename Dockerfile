FROM python:3.9


WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# ENTRYPOINT ["streamlit", "run", "project.py","--server.port=8502","--server.address=0.0.0.0"]
CMD streamlit run project.py 


