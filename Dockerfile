#Docker Image for STEP/Marmotta Webservice based on tomcat:alpine
FROM tomcat:7-jre8-alpine
MAINTAINER Alexander Wolf <al.wolf@usu.de>
#install bash
RUN apk add --update bash && rm -rf /var/cache/apk/*
#copy .war from directory
COPY marmotta.war $CATALINA_HOME/webapps
#copy necessary libs to tomcat lib folder
#COPY lib/* $CATALINA_HOME/lib
# Environment Variables
