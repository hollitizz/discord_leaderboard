FROM python:3.11

WORKDIR /app/janna

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py"]