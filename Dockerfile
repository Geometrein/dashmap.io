FROM python:3.9

WORKDIR /dashmap

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Install GDAL
RUN apt-get update --fix-missing
RUN apt install -y libgdal-dev gdal-bin python3-gdal

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy requirements.txt to Working Directory
COPY ./requirements.txt ./requirements.txt

# Install Dependecies
RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

# Copy Website Dir
COPY ./website ./website

# Copy app.py to workdir
COPY app.py ./

# Run
ENTRYPOINT [ "python3" ]
CMD ["app.py" ]
