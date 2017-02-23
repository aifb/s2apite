# S2APITE

A repository for the development of a Semantic Service API Testing Environment

# Instructions
1. Run the python script to load container, create docker-compose configuration and run everything.
Parameters are -n for number of services and -s for seed. For Example: 
```
$python s2apite.py -s 100 -n3
```
2. When finished, stop the network with:
```
$docker-compose down
```


# Requirements
- docker
- docker-compose
- python 3.x
