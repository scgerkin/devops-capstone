# Cyan App
A simple Java Spring Boot application that works as a Hello World for the Udacity Cloud DevOps
Engineer Nanodegree capstone project. It runs on the default Spring port of `8080` and serves up a static
`index.html` on the default endpoint `/`.

The project uses Maven as a  base build tool. Maven already possesses a rather robust lifecycle for
automated testing, building, and deploying. However, for the purposes of this project, each necessary
Maven `goal` is run individually using the included Jenkinsfile for use in a pipeline for
demonstration purposes.

## Build Process
Even though every stage of the Maven build can be automated using `verify`, `install`, `deploy` or
other goals, doing the build in this fashion using Jenkins allows for simpler logging and notifications
about specific failures within a build. Additionally, the added benefit of fine-tuning the build process
further using Jenkins (such as simple deployment to AWS, Docker, etc., integration with AWS services
like SNS or Lambdas) further extends the capability of building a Maven project using Jenkins rather
than the strict (and sometimes difficult to understand) Maven lifecycle.

The process includes:
- Cleaning the `target` directory of compiled sources for a fresh build
    - Artifacts should not be present already, but this adds an extra level of redundancy at little cost.
- Linting Java files according to the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html).
- Individually compiling application source code and test source code.
    - The reasoning behind this is to give feedback with regards to the specific point of failure for compilation (application sources _or_ test sources do not compile).
- Running unit tests (or any other included) with Maven test runner.
- Packaging artifacts as a `.jar` file (testing skipped as they've already run).
- Running automated tools on compiled `.class` files.
    - [SpotBugs](https://spotbugs.github.io/) for automatic detection of known bug patterns.
    - [PMD Source Code Analyzer](https://pmd.github.io/) for automatic detection of 'code smells'.
- Deploying the compiled `.jar` file(s) to an AWS S3 bucket.
- A post-build process to clean the `target` directory and free resources (regardless of build result).

