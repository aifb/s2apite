"""
s2apite configures and launches a network of semantic services in docker
"""

import argparse
import subprocess

PARSER = argparse.ArgumentParser(
    description='s2apite configures and launches a network of semantic services in docker')
PARSER.add_argument('--seed', '-s', metavar='s', type=int, required=True,
                    help='seed for random service initializer')
PARSER.add_argument('--num', '-n', metavar='n', type=int, required=True,
                    help='number of services to spawn')

ARGS = PARSER.parse_args()
print("Running s2apite: Creating " + str(ARGS.num)
      + " semantic services with seed " + str(ARGS.seed) + ".")

#create and populate docker-compose.yml file
F = open('docker-compose.yml', 'w')
print("version: '2'", file=F)
print("services:", file=F)

for i in range(ARGS.num):
    print("  marmotta" + str(i)+":", file=F)
    print("    image: registry.gitlab.com/usu-research-step/s2apite", file=F)
    print("    container_name: marmotta" + str(i), file=F)
    print("    ports:", file=F)
    print("    - \"" + str(9000 + i) + ":8080\"", file=F)
    print("    environment:", file=F)
    print("      MARMOTTAHOST: marmotta"+ str(i), file=F)

F.close()

#run docker-compose up
subprocess.call("docker-compose up -d", shell=True)

#run service initialization script

