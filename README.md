# Financial App

![Build Status](https://github.com/Karan-05/financial_app/actions/workflows/deploy.yml/badge.svg)

## Table of Contents

- [Overview](#overview)
- [Live Deployments](#live-deployments)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Local Setup (Without Docker)](#local-setup-without-docker)
  - [Docker Setup](#docker-setup)
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
    - [Docker and ECR Integration](#docker-and-ecr-integration)
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
- **GitHub Repo:** [https://github.com/Karan-05/financial_app](https://github.com/Karan-05/financial_app)

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

### Local Setup (Without Docker)

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
   ML_MODEL_PATH=path_to_your_ml_model.pkl
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

### Docker Setup

For a more streamlined setup using Docker and Docker Compose, follow these steps:

1. **Clone the Repository**

   If you haven't already, clone the repository:

   ```bash
   git clone https://github.com/Karan-05/financial_app.git
   cd financial_app
   ```

2. **Configure Environment Variables**

   Ensure you have a `.env` file in the root directory with the necessary environment variables as shown above.

3. **Build the Docker Image**

   Use Docker Compose to build the Docker image:

   ```bash
   docker-compose build
   ```

   **Explanation:**
   
   - This command reads the `docker-compose.yml` file and builds the Docker images defined therein.

4. **Run the Application with Docker Compose**

   Start the application using Docker Compose:

   ```bash
   docker-compose up -d
   ```

   **Explanation:**
   
   - The `up` command creates and starts containers based on the `docker-compose.yml` configuration.
   - The `-d` flag runs the containers in detached mode.

5. **Apply Migrations Inside the Docker Container**

   After the containers are up, apply database migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

   **Explanation:**
   
   - `web` is the name of the Django service defined in `docker-compose.yml`.
   - This command executes the migration inside the running `web` container.

6. **Access the Application**

   The application should now be running at `http://localhost:8000`.

7. **Stopping the Application**

   To stop the application, run:

   ```bash
   docker-compose down
   ```

   **Explanation:**
   
   - This command stops and removes the containers, networks, and volumes defined in the `docker-compose.yml` file.

8. **Rebuilding Containers After Code Changes**

   If you make changes to the codebase that affect the Docker image, rebuild and restart the containers:

   ```bash
   docker-compose up -d --build
   ```

   **Explanation:**
   
   - The `--build` flag forces Docker Compose to rebuild the images before starting the containers.

### Summary of Docker Commands

- **Build Images:** `docker-compose build`
- **Start Containers:** `docker-compose up -d`
- **Apply Migrations:** `docker-compose exec web python manage.py migrate`
- **Stop Containers:** `docker-compose down`
- **Rebuild and Restart:** `docker-compose up -d --build`

By using Docker and Docker Compose, you can ensure a consistent development environment across different machines and streamline the deployment process.

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

#### Docker and ECR Integration

- **Building Docker Images:**

  When a new commit is pushed, GitHub Actions uses the `Dockerfile` to build a new Docker image.

  ```bash
  docker build -t financial-app:${IMAGE_TAG} .
  ```

- **Tagging and Pushing to ECR:**

  The built image is then tagged with the ECR repository URI and pushed to Amazon ECR.

  ```bash
  docker tag financial-app:${IMAGE_TAG} 051826698008.dkr.ecr.us-east-1.amazonaws.com/financial-app:${IMAGE_TAG}
  docker push 051826698008.dkr.ecr.us-east-1.amazonaws.com/financial-app:${IMAGE_TAG}
  ```

- **Pulling Images on EC2:**

  AWS CodeDeploy triggers scripts on EC2 instances that pull the latest image from ECR and restart the Docker containers.

  ```bash
  docker pull 051826698008.dkr.ecr.us-east-1.amazonaws.com/financial-app:${IMAGE_TAG}
  docker-compose down
  docker-compose up -d --build
  ```

This integration ensures that each deployment is consistent and reproducible, leveraging Docker's containerization and ECR's secure image storage.

### Heroku Deployment

- **Access Link:** [https://fin-app-test-1e93e4768a94.herokuapp.com](https://fin-app-test-1e93e4768a94.herokuapp.com)
- **Setup:**
  - Deploys directly from the GitHub repository using Heroku's GitHub integration.
  - Utilizes Heroku's buildpacks to handle dependencies and environment configurations.
  - Managed environment variables and scaling options are configured via the Heroku dashboard.
  - Simplifies deployment by abstracting infrastructure management, allowing developers to focus solely on application code.

### Heroku vs. AWS Deployment

Choosing between Heroku and AWS for deployment depends on your project's specific needs, scalability requirements, and resource management preferences. Here's a detailed comparison to help understand the strengths and trade-offs of each platform:

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


## Acknowledgments

A heartfelt thank you to **Blockhouse** for providing this assignment. It was a great learning experience that allowed me to deepen my understanding of integrating APIs, implementing backtesting strategies, incorporating machine learning models, and automating deployments using Docker and AWS CodeDeploy. Your support and the opportunity to tackle such a comprehensive project have been invaluable.


**Feel free to reach out if you have any questions or need further assistance. Happy investing!**




# Lancey Take‑Home Challenge – Detailed Solution  
*Karan Allagh – May 20 2025*

---

## Build Instructions

```bash
g++ -std=c++17 -O2 -Wall -Wextra lancey_challenge.cpp -o lancey
```

Run the program and follow the interactive menu. All algorithms live in
`lancey_challenge.cpp`; this document explains them in depth.

---

## 1. First Non‑Repeating Character

### Algorithm

1. **Pass 1** – count occurrences in a fixed 256‑slot array (`freq`).
2. **Pass 2** – scan again; the first character whose `freq==1`
   is the answer.

*Rationale*: constant memory, two sequential passes => `O(n)` time, `O(1)` space.

### Code Excerpt

```cpp
int first_unique_index(const string& s){
    int freq[256]={0};
    for(unsigned char c: s) ++freq[c];          // pass 1
    for(size_t i=0;i<s.size();++i)              // pass 2
        if(freq[(unsigned char)s[i]]==1)
            return static_cast<int>(i);
    return -1;
}
```

### Dry Run – `"loveleetcode"`

| i | char | after pass 1 `freq[char]` | test in pass 2 |
|---|------|--------------------------|----------------|
| 0 | **l**| 1 | first with freq 1 → return 0 |

---

## 2. Vector Transform

General “map”:

```cpp
template<typename T, typename F>
auto transform_vec(const vector<T>& in, F op)
     -> vector<decltype(op(in[0]))>{
    vector<decltype(op(in[0]))> out;
    out.reserve(in.size());
    for(const T& v: in) out.push_back(op(v));
    return out;
}
```

*Why templates?* Works for any `T` and unary functor `F`.

### Dry Run – Square `[1,2,3]`

```
reserve 3
push 1→1, push 2→4, push 3→9
return [1,4,9]
```

Complexity: `O(n)` time, `O(n)` extra space (for output).

---

## 3. Domino Closed Chain

### Graph Model

Domino `[a|b]` = undirected multi‑edge between vertices `a` and `b`
(pip counts 0‑6).  
A *closed* chain exists **iff**

* graph connected on used vertices, and
* every vertex degree even → Eulerian **cycle**.

### Algorithm (Hierholzer)

1. Build adjacency `adj[v]` of **edge IDs**.
2. Reject if some `deg[v]` odd.
3. DFS:
   * Mark edge used.
   * Recurse to neighbour.
   * Push domino on **unwind** (post‑order) with correct orientation.
4. Reverse `path`.  
5. Ensure path size == `E` and ends match.

### Dry Run

Input: `[2|1] [2|3] [1|3]`

```
deg: 1:2, 2:2, 3:2 (all even)
start = 1
dfs(1) → dfs(2) → dfs(3) → dfs(1)
unwind push [3|1] [2|3] [1|2]
reverse ⇒ [1|2] [2|3] [3|1]
first.a == last.b == 1 ✔
```

Complexities: `O(E)` time, `O(E)` memory.

---

## 4. Number → English Words

### Steps

1. Split number into **chunks of 3 digits** (least‑significant first).
2. Convert each chunk with `three_digit_words`:
   * hundreds
   * tens (`twenty … ninety`)
   * teens / units
3. Append scale word (`thousand`, `million`, `billion`) based on chunk index.
4. Concatenate highest → lowest.

### Example – `12 345`

```
chunks: [345, 12]
chunk0: "three hundred forty‑five"
chunk1: "twelve thousand"
join → "twelve thousand three hundred forty‑five"
```

Special cases: 0, out‑of‑range ⇒ `"out of range"`.

Complexity: `O(log₁₀ N)` time (≤4 chunks) and `O(1)` space.

---

## 5. Queen Attack

Conditions on 8×8 board:

```cpp
bool queens_attack(pair<int,int> q1, pair<int,int> q2){
    return q1.first  == q2.first  ||   // same column
           q1.second == q2.second ||   // same row
           abs(q1.first-q2.first) ==
           abs(q1.second-q2.second);   // same diagonal
}
```

Time/space: constant.

---

## 6. Word‑Math Parser

### Grammar

```
question ::= "What is " expr "?"
expr      ::= number ( op number )*
op        ::= plus | minus | multiplied by | divided by
```

Evaluation is strictly **left‑to‑right** (spec overrides precedence).

### Algorithm

1. Validate wrapper; strip `"What is "` and trailing `?`.
2. Split tokens on spaces.
3. Helper `next_int()` parses and validates token as integer.
4. Fold:
   ```text
   acc ← first number
   for each op number:
       apply op, update acc
   ```
5. Throw `runtime_error` on syntax errors.

### Dry Run – `"What is 5 plus 13 minus 3?"`

```
tokens [5, plus, 13, minus, 3]
acc=5 → plus 13 ⇒ 18 → minus 3 ⇒ 15
return 15
```

Complexity: `O(k)` tokens.

---

## Design Reasoning

* **Manual data‑structures** (arrays, vectors) highlight algorithmic work.
* **No `std::reverse`**: I implemented `reverse_vec` to satisfy the “hands‑off” rule.
* Stored **edge ids** in domino problem – avoids pointer arithmetic UB and simplifies `used` mask.
* Recursive lambda wrapped in `std::function` to enable self‑reference in C++17.

---

## Thought Process

I tackled problems in ascending difficulty:

1. Quick wins (frequency, transform) first – build momentum.
2. Domino cycle: wrote an isolated prototype; once correct, integrated.
3. Implemented number‑words with incremental printing – tested edge cases 0, teens, scales.
4. Parser last: I hand‑rolled a loop to avoid heavy parsing libs.

Each function is **unit‑like** (stateless, no globals) → simplifies reasoning.

---

## Possible Enhancements

| Idea | Benefit |
|------|---------|
| Extend domino to Euler *trail* | solve open‑chain puzzles |
| Use `std::ranges` once C++20 allowed | cleaner transforms |
| Replace interactive menu with argument parser | script‑friendly |
| Add comprehensive unit tests | confidence, CI‑ready |

---

**End of document.**


