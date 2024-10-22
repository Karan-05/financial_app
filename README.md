# Financial App

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build Status](https://github.com/Karan-05/financial_app/actions/workflows/deploy.yml/badge.svg)

## Table of Contents

- [Overview](#overview)
- [Live Deployments](#live-deployments)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
  - [1. API Integration](#1-api-integration)
  - [2. Backtesting Logic](#2-backtesting-logic)
  - [3. Machine Learning Integration](#3-machine-learning-integration)
  - [4. Reporting](#4-reporting)
- [Deployment](#deployment)
  - [AWS Deployment](#aws-deployment)
    - [Architecture Overview](#architecture-overview)
    - [Components](#components)
    - [CI/CD Pipeline](#cicd-pipeline)
  - [Heroku Deployment](#heroku-deployment)
  - [Heroku vs. AWS Deployment](#heroku-vs-aws-deployment)
- [Evaluation Criteria](#evaluation-criteria)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

Welcome to the **Financial App** repository! This application is designed to provide users with insightful financial data analysis, leveraging robust backtesting strategies and machine learning predictions. Whether you're a financial analyst, trader, or enthusiast, this app offers powerful tools to make informed investment decisions.

## Live Deployments

- **AWS Deployment:** [http://18.215.180.207:8000](http://18.215.180.207:8000)
- **Heroku Deployment:** [https://fin-app-test-1e93e4768a94.herokuapp.com](https://fin-app-test-1e93e4768a94.herokuapp.com)

## Features

- **Real-time Financial Data Fetching:** Integrates with reliable financial APIs to fetch up-to-date market data.
- **Comprehensive Backtesting:** Implements robust backtesting strategies to evaluate investment hypotheses against historical data.
- **Machine Learning Predictions:** Utilizes pre-trained ML models to forecast market trends and asset prices.
- **Dynamic Reporting:** Generates detailed reports with visualizations and key performance metrics in both PDF and API formats.
- **Seamless Deployment:** Dockerized setup with automated CI/CD pipelines using AWS CodeDeploy and GitHub Actions.

## Technologies Used

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript (optional frameworks like React or Vue.js if used)
- **Database:** PostgreSQL
- **Containerization:** Docker
- **CI/CD:** GitHub Actions, AWS CodeDeploy
- **Cloud Platforms:** AWS EC2, Heroku
- **Machine Learning:** TensorFlow/PyTorch (depending on the model used)
- **APIs:** Financial data APIs (e.g., Alpha Vantage, IEX Cloud)
- **Reporting:** ReportLab or similar libraries for PDF generation, Matplotlib/Seaborn for visualizations

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Karan-05/financial_app.git
   cd financial_app
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory and add the following:

   ```env
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`.

## Usage

1. **Fetching Financial Data**

   Navigate to the **Data Fetching** section to retrieve the latest financial data. Ensure your API keys are correctly configured.

2. **Backtesting Strategies**

   Access the **Backtesting** module to evaluate your investment strategies against historical data. Input your parameters and run simulations to analyze performance metrics.

3. **Machine Learning Predictions**

   Utilize the **Predictions** feature to get insights based on the integrated machine learning model. Predictions are updated periodically based on new data.

4. **Generating Reports**

   Generate comprehensive reports in PDF or view them via API endpoints. Reports include visualizations and key performance indicators to aid in decision-making.

## Code Explanation

### 1. API Integration

The application integrates with financial APIs to fetch real-time and historical market data. This is handled by dedicated Django services that manage API requests, handle rate limits, and ensure data integrity.

- **Fetching Data:** Utilizes Python's `requests` library to interact with APIs like Alpha Vantage.
- **Handling Large Datasets:** Implements pagination and asynchronous requests to manage large volumes of data efficiently.
- **API Limits:** Includes error handling and retry mechanisms to gracefully handle API rate limits and downtime.

### 2. Backtesting Logic

Robust backtesting functionality allows users to test investment strategies against historical data.

- **Strategy Implementation:** Strategies are encapsulated in modular Python classes, making them easy to extend and test.
- **Performance Metrics:** Calculates returns, Sharpe ratios, drawdowns, and other key indicators to assess strategy performance.
- **Code Quality:** Written with clarity and maintainability in mind, with comprehensive unit tests ensuring reliability.

### 3. Machine Learning Integration

A pre-trained machine learning model is integrated to provide predictive analytics.

- **Model Management:** The ML model is stored as a serialized file (`.pkl`) and loaded within Django views when needed.
- **Separation of Concerns:** ML logic is encapsulated in separate modules, ensuring that Django views remain clean and focused on request handling.
- **Predictions:** Users can request predictions which are served by the ML model, offering insights into potential market movements.

### 4. Reporting

Dynamic reporting features enable users to generate insightful reports with ease.

- **PDF Generation:** Utilizes libraries like ReportLab to create well-formatted PDF reports containing visualizations and metrics.
- **API Responses:** Reports can also be accessed via API endpoints in JSON format, facilitating integration with other tools or frontend frameworks.
- **Visualizations:** Employs Matplotlib and Seaborn to create clear and informative charts and graphs, enhancing the interpretability of data.

## Deployment

The application is deployed on both AWS EC2 and Heroku, ensuring high availability and scalability. Each platform offers unique advantages tailored to different deployment needs.

### AWS Deployment

#### Architecture Overview

The AWS deployment leverages several AWS services to ensure a scalable, secure, and efficient environment for the Financial App.

![AWS Architecture](https://link-to-architecture-diagram.com)

#### Components

1. **Amazon EC2 (Elastic Compute Cloud):**
   - Hosts the Django application.
   - Configured with Docker to containerize the application for consistent deployments.

2. **Amazon ECR (Elastic Container Registry):**
   - Stores Docker images securely.
   - Acts as the central repository from which EC2 instances pull the latest images.

3. **AWS CodeDeploy:**
   - Manages automated deployments to EC2 instances.
   - Integrates with GitHub Actions to trigger deployments upon code changes.

4. **AWS S3 (Simple Storage Service):**
   - Stores deployment packages used by CodeDeploy.

5. **Security Groups and IAM Roles:**
   - Ensure secure access and permissions management.
   - IAM roles grant EC2 instances the necessary permissions to interact with ECR and other AWS services without embedding credentials.

#### CI/CD Pipeline

1. **GitHub Actions:**
   - Automates the build, test, and deployment process.
   - Upon a push to the main branch:
     - Builds the Docker image.
     - Pushes the image to Amazon ECR.
     - Packages the application for deployment.
     - Uploads the deployment package to S3.
     - Triggers AWS CodeDeploy to update the EC2 instances with the latest image.

2. **AWS CodeDeploy:**
   - Deploys the updated application to EC2 instances seamlessly.
   - Handles in-place deployments ensuring minimal downtime.

#### Deployment Steps

1. **Build and Push Docker Image:**
   - GitHub Actions builds the Docker image using the latest codebase.
   - Tags the image with the commit SHA for versioning.
   - Pushes the image to Amazon ECR.

2. **Create Deployment Package:**
   - Packages the application code along with the `appspec.yml` and deployment scripts.
   - Uploads the package to an S3 bucket.

3. **Trigger CodeDeploy:**
   - Initiates a deployment in CodeDeploy using the uploaded package.
   - CodeDeploy updates the EC2 instances by pulling the latest Docker image from ECR and restarting the Docker containers.

4. **Monitoring and Rollback:**
   - Monitors deployment success and health.
   - Automatically rolls back in case of failures to maintain application stability.

### Heroku Deployment

- **Access Link:** [https://fin-app-test-1e93e4768a94.herokuapp.com](https://fin-app-test-1e93e4768a94.herokuapp.com)
- **Setup:**
  - Deploys directly from the GitHub repository using Heroku's GitHub integration.
  - Utilizes Heroku's buildpacks to handle dependencies and environment configurations.
  - Managed environment variables and scaling options are configured via the Heroku dashboard.
  - Simplifies deployment by abstracting infrastructure management, allowing developers to focus solely on application code.

### Heroku vs. AWS Deployment

Choosing between Heroku and AWS for deployment depends on your project's specific needs, scalability requirements, and resource management preferences. Here's a comparison to help understand the strengths and trade-offs of each platform:

| Feature                   | Heroku                                             | AWS EC2 & ECR with CodeDeploy                        |
|---------------------------|----------------------------------------------------|------------------------------------------------------|
| **Ease of Use**           | Extremely user-friendly with minimal setup. Ideal for rapid deployments and small to medium projects. | Requires more setup and configuration but offers greater control and flexibility. |
| **Scalability**           | Automatically handles scaling with simple configurations. Suitable for applications with predictable scaling needs. | Highly scalable with manual or automated scaling options, suitable for large and complex applications. |
| **Cost**                  | Transparent pricing with easy-to-understand tiers. Can be cost-effective for smaller applications but may become expensive at scale. | Pay-as-you-go pricing with granular control over resources, potentially more cost-effective at scale but can be complex to manage. |
| **Flexibility**           | Limited to the features and configurations provided by Heroku. Abstracts away much of the underlying infrastructure. | Highly flexible, allowing customization of the entire stack, network configurations, and integrations with a wide array of AWS services. |
| **Deployment Speed**     | Very fast deployments with integrated CI/CD pipelines. Suitable for developers looking for quick iterations. | Slightly slower initial setup but offers robust deployment pipelines once configured. |
| **Maintenance**           | Minimal maintenance as Heroku manages the infrastructure, security patches, and scaling. | Requires managing and maintaining EC2 instances, security patches, and scaling configurations. |
| **Ecosystem Integration**| Limited to Heroku's ecosystem and available add-ons. | Seamlessly integrates with the extensive AWS ecosystem, enabling use of a vast array of services like RDS, S3, Lambda, etc. |
| **Security**              | Managed security with Heroku handling most aspects. Suitable for applications where deep security customization is not required. | Offers advanced security configurations, including VPCs, IAM roles, and security groups, providing greater control over security aspects. |
| **Learning Curve**        | Low learning curve, making it accessible for beginners or those wanting to focus solely on development. | Steeper learning curve due to the breadth of services and configurations, better suited for teams with AWS experience. |

**Recommendation:**

- **Use Heroku if:**
  - You prioritize rapid development and deployment.
  - You prefer minimal infrastructure management.
  - Your application fits within Heroku's scalability and feature offerings.

- **Use AWS EC2 & ECR with CodeDeploy if:**
  - You require greater control over your infrastructure.
  - Your application demands high scalability and customization.
  - You plan to leverage the broader AWS ecosystem for additional services and integrations.

By leveraging both platforms, you can take advantage of their unique strengths based on your project's evolving needs.

## Evaluation Criteria

This project has been developed and evaluated based on the following criteria:

1. **API Integration**:
    - Correct and efficient fetching of financial data using the specified API.
    - Proper handling of large datasets and API limits.

2. **Backtesting Logic**:
    - Robust implementation of the backtesting strategy, accurate calculation of returns and other performance metrics.
    - Code quality, clarity, and testability.

3. **ML Integration**:
    - Seamless integration of a pre-trained machine learning model for predictions.
    - Proper management of the model in Django, with clear separation of concerns (model logic vs Django views).

4. **Reporting**:
    - Clear, insightful reports with visualizations and key metrics.
    - Ability to handle both PDF generation and API responses.

5. **Deployment**:
    - Deployment is production-ready, secure, and scalable.
    - Use of Docker and CI/CD tools to automate deployment processes.

6. **Documentation**:
    - Detailed `README.md` that clearly explains how to set up and deploy the project.
    - Documentation is beginner-friendly for setup, but the task itself is designed for advanced developers.

## Acknowledgments

A heartfelt thank you to **Blockhouse** for providing this assignment. It was a great learning experience that allowed me to deepen my understanding of integrating APIs, implementing backtesting strategies, incorporating machine learning models, and automating deployments using Docker and AWS CodeDeploy. Your support and the opportunity to tackle such a comprehensive project have been invaluable.

---

**Feel free to reach out if you have any questions or need further assistance. Happy investing!**
