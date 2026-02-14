# FROM eclipse-temurin:17
# WORKDIR /app
# COPY src/ /app/src
# COPY pom.xml /app
# EXPOSE 4001
# #CMD ["java", "-jar", "demo-0.0.1-SNAPSHOT.jar"]
# CMD ["bash"]

# Build stage
FROM maven:3.9-eclipse-temurin-17-alpine AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN  mvn clean package -DskipTests


# Run stage
FROM eclipse-temurin:17
WORKDIR /app
COPY --from=build /app/target/*.jar auth-server.jar
EXPOSE 4001
CMD ["java", "-jar", "auth-server.jar"]   