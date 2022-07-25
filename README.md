
# FLask AWS Project

This is a AWS Lambda project wrapped with python flask framework. it consist of AWS Cognito for authentication and NoSQL ( DynamoDB ) for database



## Installation

```bash
  - Setup your virtual environment
  - Install required dependecies/requirements.txt
  - create an AWS account 
  - On your AWS, go to Cognito and setup a user pool account.
  - create an env file and paste your client id, pool id and region from aws
  - After installing all dependencies from requirements.txt file
  - in your project directory run 'sam init' on your terminal to setup your serverless application model 
    and follow the instructions. (NOTE: the sam template used on this project is Hello_world)
  - you can add  app.run(debug=True) on the app.py file if you want test with flask
```

## Deployment

```bash
  - Go to template.yaml on your root directory which was automaitcally created by sam
  - ( Note : Optional ) Under Events you can see the AWS API Gateway endpoints; e.g /regristration, /login etc.. 
    you can add yours and also change the request method or probably leave it.
  - on your terminal run 'sam build' to build your project for deployment
  - then run 'sam deploy' to start deploying the project to your AWS account. ( NOTE : use 'sam deploy --giuded' on the first time deployment )
  - select 'y' for yes when asked to change changeset
  - horray! your project should be successfully deployed
  
  
```


## Downloaded Dependencies

- Boto3
- Sam
- awscli
- python-dotenv


## Project Tree

```bash

├── FlaskAWS
│   ├── events
│   ├── hello_world
│   ├── ├──/app.py
│   ├── ├──/CognitoModel.py
│   ├── ├──/DatabaseModel.py
│   ├── requirements.txt

```
## Running Tests


```bash
   - Go to AWS gateway
   - click stages
   - select prod
   - use the prod url's to run your test
   - wrap your request body as a x-www-form-urlencoded
```


## Features

- Easy to run and setup
- Few dependencies 
- Pure Python, runs on Python 3.6+
- Cross platform, runs on Windows, Linux, macOS
- Code quality is maintained via continuous integration and continous deployment
- Authentication is maintained and managed by AWS Cognito
- Simpe and good loggin system with AWS CloudWatch

## Tech Stack

**Programming Languages:** Python

**Frame Work:** Python FLASK



## API Reference

```bash

 https://eq9izlp58j.execute-api.us-east-1.amazonaws.com/Prod 

 https://eq9izlp58j.execute-api.us-east-1.amazonaws.com/Prod/registration 

 https://eq9izlp58j.execute-api.us-east-1.amazonaws.com/Prod/login

 https://eq9izlp58j.execute-api.us-east-1.amazonaws.com/Prod/bank

```
    
```
## Demo

 https://eq9izlp58j.execute-api.us-east-1.amazonaws.com/Prod/


## Support

For support, email irotochukwusamuel@gmail.com

