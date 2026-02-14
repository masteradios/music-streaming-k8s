# Build stage
FROM maven:3.9-eclipse-temurin-17-alpine AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN  mvn clean package -DskipTests


# Run stage
FROM eclipse-temurin:17
WORKDIR /app
COPY --from=build /app/target/*.jar music-streaming.jar
EXPOSE 4002
CMD ["java", "-jar", "music-streaming.jar"]   