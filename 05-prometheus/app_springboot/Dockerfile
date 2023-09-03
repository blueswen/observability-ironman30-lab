FROM maven:3.8.6-openjdk-8 AS build
ADD . /build
RUN cd /build && mvn package --quiet

FROM openjdk:8-jre-slim
COPY --from=build /build/target/*.jar /app.jar
CMD ["java", "-jar", "/app.jar" ]
