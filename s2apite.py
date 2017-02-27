"""
s2apite configures and launches a network of semantic services in docker
"""
import time
import random
import base64
import argparse
import subprocess
import requests


# functions
def init_services(num, dhost):
    "Initializes the services"

    # marmotta credentials / all services use the same
    auth_base64 = base64.b64encode(b'admin:pass123').decode('ascii')

    # for i in range(10):
    #print(random.randrange(0, 5))
    #print(random.sample(["plus", "minus", "multiply", "divide"], 1))

    for i in range(num):
        port = str(9000 + i)
        name = "marmotta" + str(i)
        #dhost = "192.168.56.105"
        base_uri = "http://" + dhost + ':' + port
        print("init " + name + " on " + base_uri)

        while True:
            url = base_uri + '/marmotta/ldp/'
            try:
                status = requests.head(url, timeout=5).status_code
                if status == 200:
                    # init service
                    print("init service at marmotta")
                    headers = {'Accept': 'text/turtle',
                               'Slug': name,
                               'Content-Type': 'text/turtle',
                               'Authorization': 'Basic ' + auth_base64}
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
                               ". It can do everything you like.\" ;"
                               "	<http://step.aifb.kit.edu/hasStartAPI> child:start ;"
                               "	<http://step.aifb.kit.edu/hasProgram> child:Program1.bin ;"
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
                                   'Authorization': 'Basic ' + auth_base64}
                        payload = ("@prefix ex: <http://example.org/> ."
                                   "@prefix ldp: <http://www.w3.org/ns/ldp#> ."
                                   "@prefix step: <http://step.aifb.kit.edu/> ."
                                   "@prefix rdfs:     <http://www.w3.org/2000/01/rdf-schema#> ."
                                   "@prefix dcterms: <http://purl.org/dc/terms/> ."
                                   "@prefix foaf:    <http://xmlns.com/foaf/0.1/> ."
                                   "@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
                                   "@prefix math: <http://www.w3.org/2000/10/swap/math#> ."
                                   ""
                                   "[] ex:x \"2\" ; ex:y \"3\" ; ex:z \"4\" ."
                                   ""
                                   "{"
                                   "?point ex:x ?x ; ex:y ?y ; ex:z ?z ."
                                   "  (?x \"2\") math:exponentiation ?ex ."
                                   "  (?y \"2\") math:exponentiation ?ey ."
                                   "  (?z \"2\") math:exponentiation ?ez ."
                                   "  (?ex ?ey ?ez) math:sum ?sum ."
                                   "  ?sum math:sqrt ?sqrt ."
                                   "} => {"
                                   "  ex:result ex:value ?sqrt ."
                                   "} .")
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
                                       'Authorization': 'Basic ' + auth_base64}
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
                                       "     rdfs:label \"This starts the " + name + "\" .")
                        resp = requests.post(
                            url, headers=headers, data=payload)
                        if resp.status_code != 201:
                            print("initialization of " + name +
                                  " StartAPI failed!")
                        else:
                            print("initialization of " + name +
                                  " StartAPI successfull!")
                        break
            except requests.exceptions.Timeout:
                print("waiting for " + base_uri + " to start up...")
                time.sleep(5)


def create_dockercompose(num):
    "create and populate docker-compose.yml file"
    dcfile = open('docker-compose.yml', 'w')
    print("version: '2'", file=dcfile)
    print("services:", file=dcfile)

    for i in range(num):
        print("  marmotta" + str(i) + ":", file=dcfile)
        print("    image: registry.gitlab.com/usu-research-step/s2apite", file=dcfile)
        print("    container_name: marmotta" + str(i), file=dcfile)
        print("    ports:", file=dcfile)
        print("    - \"" + str(9000 + i) + ":8080\"", file=dcfile)
        print("    environment:", file=dcfile)
        print("      MARMOTTAHOST: marmotta" + str(i), file=dcfile)
    dcfile.close()
    print("docker compose file created")


def run_dockercompose():
    "run docker-compose command"
    subprocess.call("docker-compose up -d", shell=True)


##########################################################################
##########################################################################
###############################MAIN PROGRAMM##############################
##########################################################################
##########################################################################

# define CLI interface
PARSER = argparse.ArgumentParser(
    description='s2apite configures and launches a network of semantic services in docker')
PARSER.add_argument('--seed', '-s', metavar='s', type=int, required=True,
                    help='seed for random service initializer')
PARSER.add_argument('--num', '-n', metavar='n', type=int, required=True,
                    help='number of services to spawn')
PARSER.add_argument('--dhost', '-dh', metavar='dh', required=True,
                    help='hostname or ip of docker host')

ARGS = PARSER.parse_args()
print("Running s2apite: Creating " + str(ARGS.num)
      + " semantic services with seed " + str(ARGS.seed) + ".")


# init random with seed
random.seed(ARGS.seed)

# create docker-compose
create_dockercompose(ARGS.num)


# run docker-compose up
# run_dockercompose()

# time.sleep(5)

# run service initialization script
#init_services(ARGS.num, ARGS.dhost)
