# Cloud DevOps Nanodegree Capstone
An automated CI/CD pipeline with a blue/green deployment system.

More information is forthcoming.

## Technologies
- Jenkins for building artifacts and Docker images
- Amazon Web Services (AWS) Elastic Kubernetes Service (EKS)
- AWS CloudFormation for Infrastructre as Code
- [eksctl](https://eksctl.io) for simple(ish) management of EKS resources.

## General Information
Under Construction.

## Jenkins Component
The Jenkins service lives within a Docker container built using the items in the [jenkins](./jenkins) folder.

## Demonstration Application
The application used for demonstrating the pipeline is a simple Spring Boot application built using Maven that serves up a static website on port 8080.
