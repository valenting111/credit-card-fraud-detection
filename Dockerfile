#Which base image to use: this downloads python and its dependencies for us
FROM python:3.8

#Copy all the files in this folder to the 'app' folder (automatically created) in the container
COPY . ./app

#Set the work directory to be 'app', meaning that the command 'CMD' executed will be in context of the 'app' folder
WORKDIR /app

#Command to run to set up the container
RUN pip install -r requirements.txt

#Command to run the program. Equivalent to CMD ["python3", "api.py"]
CMD exec python3 api.py 