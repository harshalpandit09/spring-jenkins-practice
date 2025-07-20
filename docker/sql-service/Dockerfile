FROM openjdk:17-jdk-slim
WORKDIR /app
COPY sql-service.jar /app/
ENTRYPOINT ["java", "-jar", "/app/sql-service.jar"]