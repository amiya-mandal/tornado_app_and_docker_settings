
# tornado app in docker container and docker swarm as a load balancer


This app contain tornado app with mongo-DB as an database to save the data and python3 as an base.



requirements of the app:-


  * python3 [python = 3.5]
  * ubuntu (16.04)
  * mongo-DB (3.4)
  * docker (17.09.0-ce)


### setting up tornado project for testing
```
git clone https://github.com/nooby-amiya/tornado_app_and_docker_settings.git
```
now install all the requirement of the project
```
pip3 install -r req.txt
```
config mmongo db server at __port:27017__<br>
now update __app/config.py__ with your mongo-DB __Ip__ and __port__<br>
__host__ = __mongo-DB-server:IP__<br>
__port__ = __mongo-DB-server:PORT__<br>
go to app directory<br>

```
python3 maintornado.py
```  
now to check services is running hiting url <br>
```
http://localhost:8888/webpage?name=mark
```

now main task url is
```
http://localhost:8888/hotel/api?startDate=27/10/2017&endDate=14/11/2017&adults=3&children=2&source=cleartrip&City=Goa&State=Goa
```
you can change :-
  * startDate
  * endDate
  * adults
  * children
  * source (cleartrip, makemytrip)
  * City
  * State

__Note: I am working on  makemytrip data scraping but they are fetching data using post method so, it's under process__
### Now setting docker container

1. install docker
2. now we have to build docker image of our project their is a __Dockerfile__
```
docker build -t mytornadoappdeploy .
```
3. now check the container is working fine
```
docker run   -p 8888:8888 -p 27017:27017 -p 8080:8080 -p 80:80  mytornadoappdeploy
```
4. now check for the container working well
```
http://localhost:8888/webpage?name=mark
```
5. create a swarm of docker images which will balance load among them
```
docker swarm init
```
6. now we have to deploy our image in swarm
7. so in the project we have docker-composer.yml, it contain all the setting required for swarm so we run the code below
```
docker stack deploy -c docker-compose.yml mytornadoappdeploystack
```
8. for checking services<br>
```
docker service ls
docker container ls
```
9. now check for service by hitting http://localhost:8888/webpage?name=mark<br>
service is running fine<br>
__NOTE:-All load balancing is done by the docker itself, so no additional load balancing is packages or software is required, reffer here [link](http://localhost:8888/webpage?name=mark)__  

### Now for benchmark
used:
 * apache benchmark

__useage__
  *  ab -n 10000 -c 1000 http://localhost:8888/webpage?name=mark

for creating replicas check for <em>docker-composer.yml</em>

![for 1 swarm]("https://github.com/nooby-amiya/tornado_app_and_docker_settings/blob/master/deploy_on_stack_of_1.png", )
<br>
![for 5 swarm]("https://github.com/nooby-amiya/tornado_app_and_docker_settings/blob/master/deploy_on_stack_of_5.png")
<br>
![for 10 swarm]("https://github.com/nooby-amiya/tornado_app_and_docker_settings/blob/master/deploy_on_stack_of_10.png")
<br>




##### Note:- all scraping is done will edcational purpose only, so please use it for study only
