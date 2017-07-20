"""
s2apite configures and launches a network of semantic services in docker
"""
import time
import random
import base64
import argparse
import subprocess
import requests

##########################################################################
# CONSTANTS
##########################################################################

# docker image for containers
IMAGE = "aifb/s2apite:latest"
# marmotta credentials / all services use the same
AUTH = base64.b64encode(b'admin:pass123').decode('ascii')
# start time for logging timers
START = time.time()

# constants for program generator
ABC = list("abcdefghijklmnopqrstuvwxyz")
OP1NAME = {"sum": "summand", "difference": "minuend",
           "product": "multiplicant", "quotient": "dividend"}
OP2NAME = {"sum": "summand", "difference": "subtrahend",
           "product": "multiplicant", "quotient": "divisor"}
RESULTNAME = {"sum": "sum", "difference": "diff",
              "product": "prod", "quotient": "quot"}
OPERATION_VERB = {"sum": "add", "difference": "substract",
                  "product": "multiply", "quotient": "divide"}


##########################################################################
# FUNCTIONS
##########################################################################

def generate_program(operator, num_operands):
    "generates programm"
    operands = "?factors "
    operations = "(?a ?b) math:" + operator + " ?" + \
        RESULTNAME[operator] + ("1" if num_operands > 2 else "") + " .\n"
    result = ""

    operands += "   ex:" + OP1NAME[operator] + " ?a ;\n"
    for j in range(1, num_operands):
        operands += "   ex:" + OP2NAME[operator] + str(j) + " ?" + ABC[j]
        operands += ";\n" if j != num_operands - 1 else ".\n"
        if j < num_operands - 2:
            operations += "(?" + RESULTNAME[operator] + str(j) + " ?" + ABC[
                j + 1] + ")    math:" + operator + " ?" + RESULTNAME[operator] + str(j + 1) + " . \n"
    if num_operands > 2:
        operations += "(?" + RESULTNAME[operator] + str(1 if num_operands == 2 else num_operands - 2) + " ?" + ABC[
            num_operands - 1] + ")    math:" + operator + " ?" + RESULTNAME[operator] + " . \n"
    result = "   ex:result ex:value ?" + RESULTNAME[operator] + " .\n"

    program = ("@prefix ex: <http://example.org/> .\n"
               "@prefix ldp: <http://www.w3.org/ns/ldp#> .\n"
               "@prefix step: <http://step.aifb.kit.edu/> ."
               "@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .\n"
               "@prefix dcterms: <http://purl.org/dc/terms/> .\n"
               "@prefix foaf:    <http://xmlns.com/foaf/0.1/> .\n"
               "@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
               "@prefix math: <http://www.w3.org/2000/10/swap/math#> .\n"
               "{\n" + operands + "\n"
               "" + operations + "\n"
               "} => {\n"
               "" + result + ""
               "} .\n")
    return program


def generate_input_pattern(operator, num_operands):
    "generates input pattern"
    operands = "[]    "
    typedefs = ""

    equalnames = OP1NAME[operator] == OP2NAME[operator]
    operands += "ex:" + OP1NAME[operator] + \
        ("1" if equalnames == True else "") + "    ex:variable_a ;\n"
    for j in range(1, num_operands):
        operands += "ex:" + OP2NAME[operator] + (str(j + 1) if equalnames == True else str(
            j)) + " ex:variable_" + ABC[j] + (" ;\n" if j != num_operands - 1 else " .\n")
    for k in range(0, num_operands):
        typedefs += "ex:variable_" + ABC[k] + " a math:Value .\n"

    input_pattern = ("@prefix ex: <http://example.org/> .\n"
                     "@prefix ldp: <http://www.w3.org/ns/ldp#> .\n"
                     "@prefix step: <http://step.aifb.kit.edu/> .\n"
                     "@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> .\n"
                     "@prefix dcterms: <http://purl.org/dc/terms/> .\n"
                     "@prefix foaf:    <http://xmlns.com/foaf/0.1/> .\n"
                     "@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
                     "@prefix math: <http://www.w3.org/2000/10/swap/math#> .\n"
                     "\n" + 
                     "<> a <http://www.w3.org/ns/hydra/core#Operation> ."
                     "\n" + 
                     "" + operands + ""
                     "\n"
                     "" + typedefs + "")
    return input_pattern


def init_services(num, dhost):
    "Initializes the services"

    for i in range(num):
        port = str(PORT + i)
        name = "marmotta" + str(i)
        base_uri = "http://" + dhost + ':' + port
        operator = random.sample(
            ["sum", "quotient", "product", "difference"], 1).pop()
        num_operands = random.randrange(2, 26)

        print("init " + name + " on " + base_uri + "/marmotta/ldp/")
        print(name + " is a service that " +
              OPERATION_VERB[operator] + "s " + str(num_operands) + " operands.")

        pushed_successfull = {"service_container": False,
                              "service_description": False,
                              "operation": False,
                              "input_pattern": False,
                              "program": False,
                              "startapi": False}
        num_retry = 0
        countwait = 0
        url = base_uri + '/marmotta/ldp/'
        serviceContainerUrl = ""
        apiDescriptionUrl = ""
        inputPatternUrl = ""
        operationUrl = ""
        programUrl = ""
        startUrl = ""
        while True:
            try:
                resp = requests.head(url, timeout=5)
                # raise HttpError on failure
                resp.raise_for_status()
                if i == 0:
                    print("First container started after: " +
                          str(time.time() - START) + " seconds")
                
                # init service container
                if not pushed_successfull["service_container"]:
                    print("posting service container to " + url)
                    headers = {'Accept': 'text/turtle',
                               'Slug': name,
                               'Content-Type': 'text/turtle',
                               'Authorization': 'Basic ' + AUTH}
                    payload = ("@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                               "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
                               "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
                               "@prefix dcterms: <http://purl.org/dc/terms/> ."
                               #"@prefix parent: <" + base_uri + "/marmotta/ldp/> ."
                               #"@prefix child: <" + base_uri + "/marmotta/ldp/" + name + "/> ."
                               #"@prefix this: <" + base_uri + "/marmotta/ldp/" + name + "#> ."
                               ""
                               "<> a ldp:Resource , ldp:RDFSource , ldp:Container , ldp:BasicContainer ;"
                               "     rdfs:label \"This is Service " + name +
                               ". It can " +
                               OPERATION_VERB[operator] + " " +
                               str(num_operands) + " numbers.\";" +
                               "    a <http://step.aifb.kit.edu/LinkedDataWebService> ;" + 
                               "    a <http://www.hydra-cg.com/spec/latest/core/#hydra:Resource> .")
                    resp = requests.post(url, headers=headers, data=payload)
                    resp.raise_for_status();
                    serviceContainerUrl = resp.headers['Location'] + "/"  # the server determines the exact location
                    pushed_successfull["service_container"] = True
                    print("completed")

                # post input_pattern
                if not pushed_successfull["input_pattern"]:
                    print("posting input_pattern to " + serviceContainerUrl)
                    #url = base_uri + "/marmotta/ldp/" + name
                    headers = {'Accept': 'text/turtle',
                               'Slug': name + '_InputPattern',
                               'Content-Type': 'text/turtle',
                               'Authorization': 'Basic ' + AUTH}
                    payload = generate_input_pattern(operator, num_operands)
                    resp = requests.post(serviceContainerUrl, headers=headers, data=payload)
                    resp.raise_for_status()
                    inputPatternUrl = resp.headers['location'] + "/" # the server determines the exact location
                    pushed_successfull["input_pattern"] = True
                    print("completed")

                # post program
                if not pushed_successfull["program"]:
                    print("posting program to " + serviceContainerUrl)
                    #url = base_uri + "/marmotta/ldp/" + name
                    headers = {'Accept': 'text/turtle',
                               'Slug': name + '_App',
                               'Content-Type': 'text/notation3',
                               'Authorization': 'Basic ' + AUTH}
                    payload = generate_program(operator, num_operands)
                    resp = requests.post(serviceContainerUrl, headers=headers, data=payload)
                    resp.raise_for_status()
                    programUrl = resp.headers['location']  # the server determines the exact location
                    pushed_successfull["program"] = True
                    print("completed")

                # post startAPI
                if not pushed_successfull["startapi"]:
                    print("posting startAPI to " + serviceContainerUrl)
                    headers = {'Accept': 'text/turtle',
                               'Slug': name + '_Start',
                               'Content-Type': 'text/turtle',
                               'Link': '<http://www.w3.org/ns/ldp#Resource>',
                               'Authorization': 'Basic ' + AUTH}
                    payload = (#"@prefix ex: <http://example.org/> ."
                               "@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                               "@prefix step: <http://step.aifb.kit.edu/> ."
                               #"@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> ."
                               #"@prefix dcterms: <http://purl.org/dc/terms/> ."
                               #"@prefix foaf:    <http://xmlns.com/foaf/0.1/> ."
                               "@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . "
                               #"@prefix math: <http://www.w3.org/2000/10/swap/math#> ."
                               #"@prefix parent: <" + base_uri + "/marmotta/ldp/> ."
                               "<> a ldp:Resource , <http://www.w3.org/ns/hydra/core#Resource> ; "
                               "   a    step:StartApi ; "
                               #"     step:hasWebService " + apiDescriptionUrl + " ;"
                               "     rdfs:label \"This starts the service\" . ")
                    resp = requests.post(serviceContainerUrl, headers=headers, data=payload)
                    resp.raise_for_status()
                    startUrl = resp.headers['location']  # the server determines the exact location
                    pushed_successfull["startapi"] = True
                    print("completed")
                    if i == 0:
                        print("First container completely initialized after: " +
                              str(time.time() - START) + " seconds")
                    print("initialization of " + name + " StartAPI successfull")
                    
                    
                    # hydra:Operation resource
                    if not pushed_successfull["operation"]:
                        print("posting description to " + serviceContainerUrl)
                        headers = {'Accept': 'text/turtle',
                                   'Slug': name + '_Operation',
                                   'Content-Type': 'text/turtle',
                                   'Authorization': 'Basic ' + AUTH}
                        payload = ("@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                                   "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
                                   "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
                                   "@prefix dcterms: <http://purl.org/dc/terms/> ."
                                   "@prefix httpm: <http://www.w3.org/2011/http-methods#> ."
                                   #"@prefix parent: <" + base_uri + "/marmotta/ldp/> ."
                                   #"@prefix child: <" + base_uri + "/marmotta/ldp/" + name + "/> ."
                                   #"@prefix this: <" + base_uri + "/marmotta/ldp/" + name + "#> ."
                                   ""
                                   "<> a ldp:Resource , ldp:RDFSource , <http://www.w3.org/ns/hydra/core#Operation> ;"
                                   "     rdfs:label \"This is a Operation resource, specifying the behavior of " +
                                   startUrl +
                                   " . A POST request against the resource with data as specified in " +
                                   inputPatternUrl + 
                                   " will produce a result in the response body, formatted as RDF.\" ;"
                                   "    <http://www.w3.org/ns/hydra/core#method> httpm:POST  ;"
                                   "    <http://www.w3.org/ns/hydra/core#expects> <" + inputPatternUrl + "> .")
                        resp = requests.post(serviceContainerUrl, headers=headers, data=payload)
                        operationUrl = resp.headers['location']  # the server determines the exact location
                        pushed_successfull["operation"] = True
                        print("completed") 
                        
                    
                    # service description resource
                    if not pushed_successfull["service_description"]:
                        print("posting description to " + serviceContainerUrl)
                        headers = {'Accept': 'text/turtle',
                                   'Slug': name + '_ServiceDescription',
                                   'Content-Type': 'text/turtle',
                                   'Authorization': 'Basic ' + AUTH}
                        payload = ("@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                                   "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
                                   "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."
                                   "@prefix dcterms: <http://purl.org/dc/terms/> ."
                                   #"@prefix parent: <" + base_uri + "/marmotta/ldp/> ."
                                   #"@prefix child: <" + base_uri + "/marmotta/ldp/" + name + "/> ."
                                   #"@prefix this: <" + base_uri + "/marmotta/ldp/" + name + "#> ."
                                   ""
                                   "<> a ldp:Resource , ldp:RDFSource , <http://www.w3.org/ns/hydra/core#ApiDescription> ;"
                                   "     rdfs:label \"This is Service " + name +
                                   ". It can " +
                                   OPERATION_VERB[operator] + " " +
                                   str(num_operands) + " numbers.\" ;"
                                   "    <http://www.w3.org/ns/hydra/core#entrypoint> <" + startUrl + ">  ;"
                                   "    <http://step.aifb.kit.edu/hasProgram> <" + programUrl + "> ;"
                                   "    <http://www.w3.org/ns/hydra/core#operation> <" + operationUrl + "> .")
                        resp = requests.post(serviceContainerUrl, headers=headers, data=payload)
                        apiDescriptionUrl = resp.headers['location']  # the server determines the exact location
                        pushed_successfull["service_description"] = True
                        print("completed")  
                          
                    break # last resource, afterwards everything is online
                
                
            except requests.exceptions.HTTPError as ex:
                print("HTTPError: " + str(ex))
                if num_retry <= 3:
                    num_retry += 1
                    print("request " + ex.request.method + " " + ex.request.url + " failed ... retry")
                    # exponential backoff
                    time.sleep(num_retry * num_retry)
                else:
                    print("setup of " + name +
                          " unexpectedly failed! Skipping this container.")
                    print("Error " + str(ex.response.status_code) + ": " + ex.response.reason +
                          "\non request " + ex.request.method + " " + ex.request.url)
                    break
            except requests.exceptions.ConnectionError as ex:
                # this happens when the server refuses any connection yet
                print("ConnectionError: " + str(ex))
                print(base_uri + " not responding yet. waiting for start up...")
                time.sleep(5)
            except requests.exceptions.Timeout as ex:
                print("Timeout: " + str(ex))
                countwait = countwait + 1
                if countwait % 2 == 0:
                    print("waiting for " + base_uri + " to start up...")
    print("All services started and initialized after: " +
          str(time.time() - START) + "seconds")


def getlatestimage():
    "get latest version of docker image"
    subprocess.call("docker pull " + IMAGE, shell=True)


def create_dockercompose(num):
    "create and populate docker-compose.yml file"
    start_create_compose = time.time()
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
        if i > 0:
            print("    depends_on:", file=dcfile)
            print("      - marmotta" + str(i - 1), file=dcfile)
        print("    environment:", file=dcfile)
        print("      MARMOTTAHOST: marmotta" + str(i), file=dcfile)
    dcfile.close()
    print("docker compose file created in " +
          str(time.time() - start_create_compose) + " seconds")


def run_dockercompose(swarmmode):
    "run docker-compose command"
    if swarmmode:
        print("run in docker swarm")
        subprocess.call(
            "docker stack deploy -c docker-compose.yml s2apite", shell=True)
    else:
        print("run in local docker engine")
        subprocess.call("docker-compose up -d", shell=True)

##########################################################################
# MAIN PROGRAMM
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
PARSER.add_argument('-u', '--update', metavar='', type=bool, default=False,
                    help='update docker image [True/False] - default False')
PARSER.add_argument('-p', '--port', metavar='', type=int, default=9000,
                    help='first port number of port range, default: 9000')
PARSER.add_argument('-sw', '--swarm', metavar='', type=bool, default=False,
                    help='swarm mode [True/False] - default False')
ARGS = PARSER.parse_args()

print("Running s2apite: Creating " + str(ARGS.num)
      + " semantic services with seed " + str(ARGS.seed) + ".")

# UPDATE PORT
PORT = ARGS.port

# init random with seed
random.seed(ARGS.seed)

# create docker-compose
create_dockercompose(ARGS.num)

# update local image
if ARGS.update:
    getlatestimage()

# run docker-compose up
run_dockercompose(ARGS.swarm)

# wait (2 seconds for each container for initial startup)
#time.sleep(2 * ARGS.num)

# run service initialization script
init_services(ARGS.num, ARGS.dhost)