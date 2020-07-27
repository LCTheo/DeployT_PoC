# DeployT_PoC
a proof of concept for a automated service of container deployment
## who to run :
you only need a docker engine with docker-compose installed and a dns record

- first create a proxy network for Traefik with  ``` docker network create proxy```
- Set the variable ``` DNS_RECORD ``` in you shell environment to the actual dns you want to use
- complete the Treafik environment variable in the compose file under src to enable the Dns challenge (see [Traefik provider configuration](https://docs.traefik.io/v2.0/https/acme/#providers))
- run the docker-compose file with ``` docker-compose up``` 
- access to the API with the api subdomains like <http://api.my-dns.com>

## who to use :
