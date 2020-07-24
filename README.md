# DeployT_PoC
a proof of concept for a automated service of container deployment
##who to run :
you only need a docker engine with docker-compose installed and a dns record

- first create a proxy network for Traefik with  ``` docker network create proxy```
- In the docker-compose file in src directory, modify the dns on line 24 29 86 124 and 129  
- complete the Treafik environment variable to enable the Dns challenge (see [Traefik provider configuration](https://docs.traefik.io/v2.0/https/acme/#providers))
- run the docker-compose file with ``` docker-compose up``` under src
- access to the API with the api subdomains like <http://api.my-dns.com>

##who to use :
