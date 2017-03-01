"""
s2apite configures and launches a network of semantic services in docker
"""
import time
import random
import base64
import argparse
import subprocess
import requests

# constants

# docker image for containers
IMAGE = "aifb/s2apite:latest"
# first port to be used
PORT = 9000
# marmotta credentials / all services use the same
AUTH = base64.b64encode(b'admin:pass123').decode('ascii')
# start time for logging timers
START = time.time()

# functions
def init_services(num, dhost):
    "Initializes the services"

    # for i in range(10):
    #print(random.randrange(0, 5))
    #print(random.sample(["plus", "minus", "multiply", "divide"], 1))

    for i in range(num):
        port = str(PORT + i)
        name = "marmotta" + str(i)
        #dhost = "192.168.56.105"
        base_uri = "http://" + dhost + ':' + port
        operator = random.sample(["sum", "quotient", "product", "difference"], 1).pop()
        operator_verb = "add"
        num_operands = random.randrange(2, 10)
        if operator == "quotient":
            operator_verb = "divide"
        if operator == "product":
            operator_verb = "multiply"
        if operator == "negate":
            operator_verb = "substract"
        print("init " + name + " on " + base_uri + "/marmotta/ldp/")
        print(name + "is a service that " + operator_verb + "s " +  str(num_operands) + " operands.")
        
        countwait = 0
        while True:
            url = base_uri + '/marmotta/ldp/'
            try:
                status = requests.head(url, timeout=5).status_code
                if status == 200:
                    if(i == 1): 
                        print("First container started after:" + str(time.time() - START))
                    # init service
                    print("init service at " + name)
                    headers = {'Accept': 'text/turtle',
                               'Slug': name,
                               'Content-Type': 'text/turtle',
                               'Authorization': 'Basic ' + AUTH}
                    payload = ("@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                               "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
                               "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
                               "@prefix dcterms: <http://purl.org/dc/terms/> ."
                               "@prefix parent: <" + base_uri + "/marmotta/ldp/> ."
                               "@prefix child: <" + base_uri + "/marmotta/ldp/" + name + "/> ."
                               "@prefix this: <" + base_uri + "/marmotta/ldp/" + name + "#> ."
                               ""
                               "<> a ldp:Resource , ldp:RDFSource , ldp:Container , ldp:BasicContainer ;"
                               "     rdfs:label \"This is Service " + name +
                               ". It can "+ operator_verb + " numbers.\" ;"
                               "	<http://step.aifb.kit.edu/hasStartAPI> child:start ;"
                               "	<http://step.aifb.kit.edu/hasProgram> child:" + name + "app.bin ;"
                               "	a <http://step.aifb.kit.edu/LinkedDataWebService> .")
                    resp = requests.post(url, headers=headers, data=payload)
                    if resp.status_code != 201:
                        print("setup of " + name + " failed!")
                    else:
                        print("setup of " + name + " successfull!")
                        # post program
                        print("pushing programm to marmotta service")
                        url = base_uri + "/marmotta/ldp/" + name
                        headers = {'Accept': 'text/turtle',
                                   'Slug': name + "app",
                                   'Content-Type': 'text/notation3',
                                   'Authorization': 'Basic ' + AUTH}
                        payload = ("@prefix ex: <http://example.org/> ."
                                   "@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                                   "@prefix step: <http://step.aifb.kit.edu/> ."
                                   "@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> ."
                                   "@prefix dcterms: <http://purl.org/dc/terms/> ."
                                   "@prefix foaf:    <http://xmlns.com/foaf/0.1/> ."
                                   "@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
                                   "@prefix math: <http://www.w3.org/2000/10/swap/math#> ."
                                   "[] ex:x \"2\" ; ex:y \"3\" ."
                                   "{"
                                   "  ?factors ex:x ?x ; ex:y ?y ."
                                   "  (?x ?y) math:" + operator + " ?result ."
                                   "} => {"
                                   "  ex:result ex:value ?result ."
                                   "} .")

                        #sum, quotient, product, negation
                        resp = requests.post(
                            url, headers=headers, data=payload)
                        if resp.status_code != 201:
                            print("intallation of programm at " +
                                  name + " failed!")
                        else:
                            print("intallation of programm at " +
                                  name + " successfull!")
                            # post program
                            print("pushing startAPI to " + name)
                            url = base_uri + "/marmotta/ldp/" + name
                            headers = {'Accept': 'text/turtle',
                                       'Slug': "start",
                                       'Content-Type': 'text/turtle',
                                       'Authorization': 'Basic ' + AUTH}
                            payload = ("@prefix ex: <http://example.org/> ."
                                       "@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                                       "@prefix step: <http://step.aifb.kit.edu/> ."
                                       "@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> ."
                                       "@prefix dcterms: <http://purl.org/dc/terms/> ."
                                       "@prefix foaf:    <http://xmlns.com/foaf/0.1/> ."
                                       "@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
                                       "@prefix math: <http://www.w3.org/2000/10/swap/math#> ."
                                       "@prefix parent: <http://localhost:8080/marmotta/ldp/> ."
                                       "<> a ldp:Resource ; a step:StartAPI ;"
                                       "     step:hasWebService parent:" + name + " ;"
                                       "     rdfs:label \"This starts the " + name + "app\" .")
                        resp = requests.post(
                            url, headers=headers, data=payload)
                        if resp.status_code != 201:
                            print("initialization of " + name +
                                  " StartAPI failed!")
                        else:
                            print("initialization of " + name +
                                  " StartAPI successfull!")
                        countwait = 0
                        break
            except requests.exceptions.Timeout:
                countwait = countwait + 1
                if countwait % 100 == 0:
                    print("waiting for " + base_uri + " to start up...")
                time.sleep(.01)


def getlatestimage():
    "get latest version of docker image"
    subprocess.call("docker pull " + IMAGE, shell=True)   

def create_dockercompose(num):
    "create and populate docker-compose.yml file"
    dcfile = open('docker-compose.yml', 'w')
    print("version: '3'", file=dcfile)
    print("services:", file=dcfile)

    for i in range(num):
        print("  marmotta" + str(i) + ":", file=dcfile)
        print("    image: " + IMAGE, file=dcfile)
        # container name not supported in swarm deployment / v3
        #print("    container_name: marmotta" + str(i), file=dcfile)
        print("    ports:", file=dcfile)
        print("    - \"" + str(PORT + i) + ":8080\"", file=dcfile)
        print("    environment:", file=dcfile)
        print("      MARMOTTAHOST: marmotta" + str(i), file=dcfile)
    dcfile.close()
    print("docker compose file created")


def run_dockercompose(swarmmode):
    "run docker-compose command"
    if swarmmode:
        print("run swarm")
    #subprocess.call("docker stack deploy -c docker-compose.yml s2apite", shell=True)
    else:
        print("run normal")
    #subprocess.call("docker-compose up -d", shell=True)


##########################################################################
##########################################################################
###############################MAIN PROGRAMM##############################
##########################################################################
##########################################################################

# define CLI interface
PARSER = argparse.ArgumentParser(
    description='s2apite configures and launches a network of semantic services in docker')
PARSER.add_argument('-s', '--seed', type=int, metavar='', required=True,
                    help='seed for random service initializer')
PARSER.add_argument('-n', '--num', type=int, metavar='', required=True,
                    help='number of services to spawn')
PARSER.add_argument('-dh', '--dhost', metavar='', required=True,
                    help='hostname or ip of docker host')
PARSER.add_argument('-p', '--port', metavar='', type=int, default=PORT,
                    help='first port number of port range, default: ' +str(PORT))
PARSER.add_argument('-sw', '--swarm', metavar='', type=bool, default=False,
                    help='swarm mode [True/False] - default False')

ARGS = PARSER.parse_args()

print("Running s2apite: Creating " + str(ARGS.num)
      + " semantic services with seed " + str(ARGS.seed) + ".")

PORT = ARGS.port

# init random with seed
random.seed(ARGS.seed)

# create docker-compose
create_dockercompose(ARGS.num)

# update local image 
#getlatestimage()

# run docker-compose up
run_dockercompose(ARGS.swarm)

#time.sleep(5)

# run service initialization script
#init_services(ARGS.num, ARGS.dhost)
