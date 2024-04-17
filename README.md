# k8s_system_design - Video to MP3 Converter Service

## Project Overview

This project leverages Kubernetes to orchestrate a microservice architecture designed to convert videos to MP3 format. Utilizing the scalability and management features of Kubernetes, this service aims to efficiently process video files and extract audio content.

## Architecture

System Diagram
![System Diagram](Images/system_design.png "System Diagram")

In total there are 5 microservices and 2 databases

Microservices:

- Gateway: Clients interacts with this service which in turn relays request to all the other services
- Auth: Handles the authorization and authentication of any client trying to access the system.
- Converter: Converts videos to mp3s, ingesting new videos from the rabbitmq qs.
- Rabbit: Queues which allows for asynchronous interservice communication.
- Notification: Shoots a message to client's email with a mp3_id on completion of conversion to mp3.

Databases:

- MySQL: Contains auth db, which has users table containing username and password for authorization and authentication.
- MongoDb: Contains videos and mp3s db

## Getting Started

### Prerequisites

- Kubernetes
- Docker
- MySQL
- MongoDb

### Deployment

Instructions on how to deploy the microservices on Kubernetes:

1. Build Docker images for the microservices.
2. Configure Kubernetes resources (e.g., Deployments, Services, ConfigMaps, Secrets).
3. Apply the Kubernetes configurations to your cluster.
4. Verify the deployment.

## Usage

How to use the service:

- Endpoints to interact with the service.
- Example requests and responses.

## Authors

- Jay Joshi
