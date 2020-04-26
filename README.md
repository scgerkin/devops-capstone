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

## Demonstration Application - "Cyan App"
### When you combine blue with green, the resultant color is cyan. Hence, Cyan App!
This is the application being built and deployed by the CI/CD pipeline. It is a
simple Java Spring Boot application that serves up a static
[`index.hmtl`](./src/main/resources/templates/index.html) using ThymeLeaf templating. The application originally has a blue background to indicate that it
is the original application during deployment in the blue/green deployment scheme.

The project uses Maven as a  base build tool. Maven already possesses a rather robust lifecycle for automated testing, building, and deploying. However, for
the purposes of this project, each necessary Maven `goal` is run individually
in Jenkins for demonstration and incremental testing while constructing the
full pipeline.

### Build Process
The build process with Maven is meant only as a demonstration. Ideally, we would want to use the
[Maven Release Plugin](http://maven.apache.org/maven-release/maven-release-plugin/) to manage our
deployments and automate versioning the application. As this project is meant as a demonstration for
Jenkins and automatic deployments with EKS, the build process for the `.jar` artifact is very rudimentary
and broken down into a few extra pieces to highlight the actions taken by Jenkins.

The process includes:
- Cleaning the `target` directory of compiled sources for a fresh build
    - Artifacts should not be present already, but this adds an extra level of redundancy at little cost.
- Linting Java files according to the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html).
    - Any failure in linting will cause an early failure of the pipeline, but it would be better to automate linting and fixing small problems where possible.
- Compiling application source code and test source code.
- Running unit tests written in jUnit with the Maven test runner.
    - At this point, we would also want to consider outputting the results into a file (particularly for failure).
- Packaging artifacts as a `.jar` file.
- Running automated tools on compiled `.class` files.
    - [SpotBugs](https://spotbugs.github.io/) for automatic detection of known bug patterns.
    - [PMD Source Code Analyzer](https://pmd.github.io/) for automatic detection of 'code smells'.
- A post-build process to clean the `target` directory and free resources (regardless of build result).
