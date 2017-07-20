#Docker Image for STEP/Marmotta Webservice based on tomcat:alpine
FROM tomcat:7-jre8-alpine
MAINTAINER Alexander Wolf <al.wolf@usu.de>
#install bash
RUN apk add --update bash && rm -rf /var/cache/apk/*
#copy .war from directory
COPY marmotta.war $CATALINA_HOME/webapps
#copy necessary libs to tomcat lib folder
RUN curl  http://linked-data-fu.github.io/releases/0.9.10/linked-data-fu-standalone-0.9.10-bin.tar.gz \
| tar -xjC /tmp/linked-data-fu-standalone-0.9.10
RUN cp /tmp/linked-data-fu-standalone-0.9.10/lib/linked-data-fu* $CATALINA_HOME/lib
RUN rm -R /tmp/linked-data-fu-standalone-0.9.10
# Environment Variables
