# credit-card-fraud-detection
Building and deploying a credit card fraud detection ML algorithm


### Dataset
The dataset used is available at https://www.kaggle.com/mlg-ulb/creditcardfraud. It is a table containing credit card transactions, classified as fraudulent or valid transactions. The features are the result of PCA applied to raw user information that we do not have access to, together with the Amount of the transactions and the Time elapsed since the first transaction in the dataset. There are 284807 data samples in total.

### Challenge
The difficulties when tackling a fraud detection task is the unavailability of a lot of fraud examples (huge class imbalance). This means that more elaborate metrics need to be used (precision, recall, f1 score, confusion matrix) together with advanced classification techniques.

### Models tested
Several models are tested.

The algorithms are:
- Logistic Regression
- Support Vector Machines
- Gaussian Mixture Model
- Isolation Forest
- Local Outlier Factor

### Deployment
The best model is then deployed as an app using the FastAPI library. The app is containerized using Docker and is made available globally using Google Cloud Platform.

##### Deployment: Sending and receiving data

To test the model, we need to send data to the app, make a prediction with our trained model, and send back the prediction. This transfer of data is done using the Pydantic library (with FastAPI) and its `BaseModel` class. We create our own classes for data sent to the server (simply the list of features and their values of a new sample) and data received by the server (the class predicted) by inheriting from this class.

The simplest way to send raw data to be converted by these custom classes is to use the JSON format: In Python, this is just a dictionary where keys are the attributes' names expected by the Pydantic model and the values are the corresponding (numerical) values.

**Note**: You can send requests to the api directly from your terminal using cURL. 
##### Simple intro to cURL 
It is a command line tool that allows data transfers across the internet. To make a get request to a url `myurl`, from the command line type: `curl myurl`.
The get method is used by default. 
To change it, use `-X`:
`curl -X GET myurl`
`curl -X POST myurl` (though we need to send data in that case, see below)

For a post request, we need to send data. This can be done with `-d` or `--data`. The following parameter has to be the data being sent, and can take multiple forms:
- Give parameter values (here for parameters **option** and **something**): `curl -X POST -d "option=somevalue&something=othervalue" myurl`
- Give data in JSON format: For specific data formats (like JSON), it is important to specify the format in the POST request, otherwise the operation might not execute successfully. This means specifying the data is an image, an audio file or a JSON file. To do this, use `-H`, which is equivalent to using `--header`, followed by a string indicating the content type of the data sent: `" Content-Type: application/json "` or "Content-Type: image/jpeg" for example. Finally, to tell that the data is saved in a file rather than directly written in the CLI, use **@filename**.
 In this project, we send a new input sample in JSON format saved in the **test_data.json** file. So the corresponding post request is: 
 `curl -X POST -H "Content-Type: application/json -d @test_data.json http://localhost:8000/predict`.


