
# Hi, I'm Omar Shindy 
Assistant Lecturer/Software Engineer/Data Engineer.

In this repo you will find the basic instructions needed to run this project.
The project idea is mainly focused on showing my Data Engineering skills, the project is about extracting data from third party api and building data lake using ETL basic process.


## Setting up the development environment

- After cloning the repo please add .env file containing variable appID containing the API token your for https://openexchangerates.org/ app. 

- Navigate to breadfast-task directory then create a virtual environment.

- Activate the virtual environment.

- Run the following code to install all the dependencies needed to run the pipline
 ```
    pip install -r requirment.txt
```

### The Expected output

A new directory named exchange-rates will be created into your main directory containes another directory named 2022 containes current month name ex: april contains the extracted csv file with the current day exchange rate ex: 20.csv


## Testing

I wrote some manual test cases depends on faking create a list of dates passing this list to the main class created and performing the ETL functions from this class to test over Historical data pulled from the API.

In Testing folder you will find the requirment.txt file contains the dependecies needed for testing and already tested files gathering historical data from the API
