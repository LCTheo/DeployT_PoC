# DeployT_PoC
a proof of concept for a automated service of container deployment
## who to run :
you only need a docker engine with docker-compose installed and a dns record

- First create a proxy network for Traefik with  ``` docker network create proxy```
- Change the variable ``` DNS_RECORD ``` in the .env file 
- Set a wild card entry in your dns table of your dns record like ```*.my-dns.com```
- Complete the Treafik environment variable in the docker-compose.yml file under src to enable the Dns challenge (see [Traefik provider configuration](https://docs.traefik.io/v2.0/https/acme/#providers))
- Change the provider under traefik/traefik.yml if necessary
- Run the docker-compose file with ``` docker-compose up``` 
- Access to the API with the api subdomains like <http://api.my-dns.com>

## who to use :
- go to ``` api.my-dns.com ``` and register with ```/api/user/registration``` to start using the api
