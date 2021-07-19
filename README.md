# credit-card-fraud-detection
Building and deploying a credit card fraud detection ML algorithm


### Dataset
The dataset used is available at https://www.kaggle.com/mlg-ulb/creditcardfraud. It is a table containing credit card transactions, classified as fraudulent or valid transactions. The features are the result of PCA applied to raw user information that we do not have access to, together with the Amount of the transactions and the Time elapsed since the first transaction in the dataset. There are 284807 data samples in total.

### Challenge
The difficulties when tackling a fraud detection task is the unavailability of a lot of fraud examples (huge class imbalance). This means that more elaborate metrics need to be used (precision, recall, average accurach, f1 score, confusion matrix) together with advanced classification techniques.

### Models tested
Several models are tested.

The algorithms are:
- Logistic Regression
- Support Vector Machines
- Gaussian Mixture Model
- Isolation Forest

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

 #### Deploying locally with Python vs locally with Docker vs globally with Docker and GCP


 Deploying the app on your local computer is simpler than deploying it remotely.

 The simplest way to launch the app locally is to execute from the command line:
 `python3 api.py`

 In that case, the domain is set to "0.0.0.0" (equivalent to "localhost" or "127.0.0.1"), and the port is set to either the port's environment variable value (if it exists) or 8000 otherwise, using `os.environ.get('PORT', 8000)`.

 This whole project/app can be containerized using Docker, to simplify its reusability across devices and platforms. Note that unlike in many online repositories, the command CMD we run doesn't use uvicorn or gunicorn but the same python3 command, and doesn't specify any additional parameters. This is done on purpose as I think it's more intuitive to keep consistency between the different methods used to run our app, by always using the same start-up command. 
 However, because our app is now running in a container, we need to map (<=> publish) the host's port (port on our computer) to the container's port in order for the app to run. Therefore, when running the app locally we need to set the `-p` flag, which stands for publish. Running the app is therefore done using the two following commands:
 - Building the image: `docker build -t fraud_image .` (tag the image to have an intuitive name)
 - Run it in a container: `docker run -p 8000:8000 fraud_image`

 Finally, deploying to Google Cloud Platform takes a bit more time (but not that much). 
Make sure you have a GCP account set up and you've installed the gcloud sdk, and then type:
`gcloud init`
Follow the instructions to set up the GCP project you'll use to deploy your app.

Deploying our app to the GCP requires 2 steps, as when using Docker on your local machine: 
 1) Build the image of our app and store it in Google Container Registry. This is done with:
 `gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/IMAGE-NAME`
 2) Run the image in a container. This is done with:
  `gcloud run deploy --image gcr.io/YOUR-PROJECT-ID/IMAGE-NAME`

 The main issue you need to bear in mind when deploying an API on a web server is the handling of URL ports. Unfortunately, you cannot set the **publish** flag directly. Depending on which Google's resource you use to deploy your app, you will need to use different solutions. If deploying using Google Cloud Run, the documentation (https://cloud.google.com/run/docs/configuring/containers#console) explains the options available.

 The 2 options I've tried are:

 - **Set the PORT environment variable**: This is done with `port=os.environ.get('PORT', 8000)` in the last line of `api.py` and is sufficient to make the container's port available to the outside world without modifying the gcloud commands.

 - **Set the port flag in the google cloud CLI**: If instead of `port=os.environ.get('PORT', 8000)` you just assign an integer value to port, such as `port=8000`, then this will not be successfully interpreted by Google Cloud Run (aka it will crash). One simple fix is by setting the PORT environment variable in the CLI, with:
   `gcloud run deploy --image gcr.io/YOUR-PROJECT-ID/IMAGE-NAME --port 8000`








