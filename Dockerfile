# Use an official Python runtime as a parent image
#FROM python:3.5

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD app /app

# Install any needed packages specified in requirements.txt
# RUN pip install -r req.txt

# I am unable to install the requirement from file so i am using old method
RUN pip install ujson
RUN pip install tornado
RUN pip install future
RUN pip install requests
RUN pip install pymongo

# Make port 8888 available to the world outside this container
EXPOSE 8888
EXPOSE 80
EXPOSE 8080
EXPOSE 32768

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "/app/maintornado.py"]

# Set proxy server, replace host:/port with values for your servers
ENV http_proxy host:/port
ENV https_proxy host:/port



# Forward chain between docker0 and eth0
#iptables -A FORWARD -i docker0 -o eth0 -j ACCEPT
#ptables -A FORWARD -i eth0 -o docker0 -j ACCEPT

# IPv6 chain if needed
#ip6tables -A FORWARD -i docker0 -o eth0 -j ACCEPT
#ip6tables -A FORWARD -i eth0 -o docker0 -j ACCEPT


# Log dropped outbound packets
#iptables -N LOGGING
#iptables -A OUTPUT -j LOGGING
#iptables -A INPUT -j LOGGING
#iptables -A FORWARD -j LOGGING
#iptables -A LOGGING -m limit --limit 2/min -j LOG --log-prefix "IPTables-Dropped: " --log-level 4
#iptables -A LOGGING -j DROP