#Definir imagen base
FROM ubuntu:20.04

#Definir qué ejecutar al crear la imagen
RUN apt-get update -y && apt-get install --y python3-pip python3-dev vim-tiny

#Copiar ficheros 
COPY ./requirements.txt /sec_framework-frontend/requirements.txt

#Establecer directorio de trabajo
WORKDIR /sec_framework

RUN pip install -r requirements.txt

COPY . /sec_framework-frontend/

ENV FLASK_APP="app/app.py"
ENV FLASK_ENV="development"

CMD [ "flask", "run", "--host=0.0.0.0"]