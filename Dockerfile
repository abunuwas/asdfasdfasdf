FROM ubuntu:latest
 
# Update OS
RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y upgrade
 
# Install Python
RUN apt-get install -y python3-pip python3.5

# Add requirements.txt
ADD requirements.txt /application/
 
# Install uwsgi Python web server
RUN pip3 install uwsgi
# Install app requirements
RUN pip3 install -r application/requirements.txt

# Create app directory
ADD config /application/config
ADD src /application/src

RUN cd /application/config && ls

# Set the default directory for our environment
ENV HOME /application
WORKDIR /application/src

# Expose port 5001 for uwsg
EXPOSE 5001
 
ENTRYPOINT ["python3", "application.py"]