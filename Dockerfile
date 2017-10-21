FROM ubuntu:16.04

RUN apt-get update
RUN apt-get upgrade
# python 3 installer and dep in ubuntu 16.40
RUN apt-get install -y python3.5
RUN apt-get install -y python3-pip
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev

# making directory
RUN mkdir app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app /app

# Install any needed packages specified in requirements.txt
# RUN pip3 install -r req.txt

# I am unable to install the requirement from file so i am using old method
RUN pip3 install --upgrade pip
RUN pip3 install ujson
RUN pip3 install tornado
RUN pip3 install future
RUN pip3 install requests
RUN pip3 install pymongo

# Make port 8888 available to the world outside this container
EXPOSE 8888
EXPOSE 80
EXPOSE 8080
EXPOSE 27017

# Define environment variable
ENV NAME World
RUN cd /app

# Run app.py when the container launches
CMD ["python3", "maintornado.py"]

# Set proxy server, replace host:/port with values for your servers
ENV http_proxy host:/port
ENV https_proxy host:/port
