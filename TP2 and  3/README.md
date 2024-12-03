# EPF-API-TP

- **Question 1:** _Which Python library/framework is often used to create fast, simple REST APIs?_

  - Django

  - Flask

  - **FastAPI**

  - All of the above

- **Question 2:** _What's the main difference between Django, Flask and FastAPI in terms of performance and speed?_

  - Django is generally faster than Flask and FastAPI.

  - Flask outperforms Django and FastAPI.

  - **FastAPI is renowned for its increased speed and performance compared with Django and Flask.**

  - Django, Flask and FastAPI have equivalent performance.

- **Question 3:** What is an endpoint in the context of REST APIs?\*

  - A unique IP address associated with an API.

  - A breakpoint in the code where the API can be interrupted.

  - **A specific URL to which a request can be sent to interact with the API.**

  - A unique identifier assigned to each incoming request.

- **Question 4:** _What are the main HTTP verbs used to define REST API methods?_

  - **GET, POST, PUT, PATCH, DELETE**

  - SEND, RECEIVE, UPDATE, REMOVE

  - READ, WRITE, MODIFY, DELETE

  - FETCH, INSERT, UPDATE, DELETE

- **Question 5:** _In the context of REST APIs, what does the term "middleware" mean?_

  - A component that processes data sent by the user.

  - An external library used to speed up API development.

  - **Intermediate software that processes the request before it reaches the main application.**

  - A method for securing data stored in the database.

- **Question 6:** _Which Python library is often used to serialize and deserialize JSON data in the context of REST APIs?_

  - JSONify

  - PyJSON

  - **json.dumps() and json.loads()**

  - serializeJSON

- **Question 7:** _What is the main use of the HTTP "PUT" method in the context of REST APIs?_

  - Create a new resource.

  - **Update an existing resource, or create one if it doesn't exist.**

  - Delete a resource.

  - Read a specific resource.

- **Question 8:** In FastAPI, how do you define an endpoint to handle a POST request with JSON data?\*

  - **@app.post("/endpoint")**

  - @app.get("/endpoint")

  - @app.request("/endpoint")

  - @app.update("/endpoint")

# Creating an API with FastAPI

### Introduction

In this exercise you are going to encapsulate data processing and machine learning model execution logic to make predictions on a well-known dataset: iris kaggle dataset

### Few elements to remember about the REST Protocol

REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs (Application Programming Interfaces) conform to the principles of REST, allowing systems to communicate over HTTP in a stateless manner; Some important aspects are:

- **Resources:** Everything is a resource, identified by a unique URI.

- **HTTP Methods:** CRUD operations are performed using standard HTTP methods (GET, POST, PUT, DELETE).

- **Stateless:** Each request from a client contains all the information needed to understand and fulfill the request.

### Key Concepts in FastAPI:

- **Endpoint:**

- **Basic HTTP Methods:**

- **Request and Response:**

### Evaluation requirements

The evaluation criteria will be as follows:

- Proper functioning of endpoints
- Clear documentation of code, use of explicit names and compliance with REST naming conventions. Please follow pep-8 convention for documenting your functions (exemple at the end of the README)
- Static swagger generation through an API route
- Completion of unit tests

### Objective

Before starting the exercise, fork the following git repo if not already done in TP1: https://github.com/klem-data/API---Webscrapping \
Don't forget to add me to the repo with the following email address: clement.letizia1@epfedu.fr

About the API workflow:
- The router.py file contains references to the routers defined in the routers folder.
- The routers file contains the declaration of all API routes by tags 
- The Services folder must contain the functions that are called in the route declaration

- **Step 1: Installing libraries:** Install the libraries in the requirements.txt

- **Step 2: First launch:**  Execute the main.py file in the root folder and access it.

- **Step 3: Redirect root API:**  Redirect the root endpoint of your API to the automatic swagger documentation

- **Step 4: Access the swagger documentation:**  Access to the swagger built automatically by FastAPI

- **Step 5: First call to the API:**  Make an API request on the hello route using the swagger directly or a tool like insomnia or postman

- **Step 6: Access the dataset:**  Create a route in api/routes/data to download and save the contents of the following kaggle dataset in the src/data folder: https://www.kaggle.com/datasets/uciml/iris. If you're having too many problems, simply download the dataset from the kaggle website. documentation : https://www.geeksforgeeks.org/how-to-download-kaggle-datasets-into-jupyter-notebook/

- **Step 7: Loading the Iris Flower dataset:** Add an endpoint to load the iris dataset file as a dataframe and return it as a json.

- **Step 8: Processing the dataset:** Add an endpoint to be able to perform the necessary processing on the data before being able to train a model with it.

- **Step 9: Split in train and test:** Add an endpoint to split the iris dataset as train and test and send back a json with both

- **Step 10: Parameters init:** Go to scikit learn and select any classification model to be used on the iris dataset (performance is of no interest to us in this course). Look at the parameters you need to use for this model and store them in the file src/config/model_parameters.json

- **Step 11: Training the classification model:** Add an endpoint to train a classification model with the processed dataset as input and saved this model in the folder src/models.

- **Step 12: Prediction with Trained Model:** Add endpoint to make predictions with trained model and parameters. This endpoint have to send back the predictions as json.

- **Step 13: Create the Firestore collection:** Create the firestore collection "parameters" with the following parameters: "n_estimators", "criterion". The name of the document with the parameters have to be : parameters.

- **Step 14: Retrieve parameters from Firestore:** Add an endpoint to retrieve parameters from Firestore.

- **Step 15: Update and add Firestore parameters:** Add endpoints to update or add parameters in Firestore.

- **Step 16: Authentication:** Implement authentication through Firestore authentication

- **Step 17: User management:** Extend authentication to include user registration, login and logout endpoints. Explore also user roles and permissions. Allow only admin users to access to the list of user 

- **Step 18: Protection against Denial of Service (DoS) attacks:** Implement rate limiting by user

- **Step 19: API versioning:** Add the information about the version of your API. (you are on version 1.0) Also add the prefix to your routes to indicate the version.

- **Step 20: Error Handling:** Add a custom error responses for error 404 and provide meaningful error message.

- **Step 21: API testing:** Implement unit tests for your functions and enpoints

- **Step 22: CI/CD pipeline:** Define a CI/CD pipeline on github using github Actions to launch your tests after every push

The completion of this TP is relatively long and may overtake TP3 

### Documentation link :

- FastApi: https://fastapi.tiangolo.com/

- Google Cloud Firestore: https://cloud.google.com/python/docs/reference/firestore/latest/index.html

- Scikit-Learn: https://scikit-learn.org/stable/index.html

- Pandas: https://pandas.pydata.org/docs/


### Pep-8 docstring example :

"""
  Retrieve content of a json file

  Args:
      path (str): The path of the file

  Returns:
      JSON object: The json object with the parameters
  """
