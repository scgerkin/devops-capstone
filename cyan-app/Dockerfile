FROM openjdk:14-jdk-alpine
# Full name and extension, ie app.jar
ARG jarName
ENV JAR $jarName
ADD target/$jarName /$jarName
EXPOSE 8080
ENTRYPOINT java -jar $JAR
