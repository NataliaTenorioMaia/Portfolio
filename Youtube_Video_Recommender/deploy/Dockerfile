# selects the image:
FROM python:3.8-slim
# creates a directory inside our container:
RUN mkdir /myapp
# sets the working directory:
WORKDIR /myapp
# copies all files from current folder to our working directory:
COPY . .
# updates and installs some libraries that we need to run LightGBM:
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        cmake \
        build-essential \
        gcc \
        g++
# installs in the container some python modules in the versions that we used in our app:
RUN pip install -r requirements.txt
# this updates our video database:
RUN python db_starter.py
# executes the green unicorn server:
CMD gunicorn --bind 0.0.0.0:$PORT wsgi 

# For explanation of some basic commands: https://www.fosstechnix.com/dockerfile-instructions/
