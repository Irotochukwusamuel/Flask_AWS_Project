from flask_lambda import FlaskLambda
from DataBaseModel import Table
from CognitoModel import Cognito
from flask import request
import json

app = FlaskLambda(__name__)  # This wraps the lambda function with flask to make it easier to make http request

table = Table()  # instantiating the Table model

Auth = Cognito()  # instantiating the cognito model


def responseJSON(message):
    """
    This handles the response from server side.

    :param message:
    :return: json
    """
    return (
        json.dumps({'response': message}),
        200,
        {'Content-Type': 'application/json'}
    )


@app.route('/')
def Health():
    """
    Test the Health of the API, if it is live and working well
    :return: json
    """
    data = {
        "message": "Hi! the API is Live and you are good to test. Please encode you POST request body as x-www-form-urlencoded"
    }
    return responseJSON(data)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    """
    Handles the user registration.
    NOTE : it only accepts a POST Method
    :return: json
    """

    if not request.method == "POST":
        return responseJSON('Only Post method is supported')

    User = table.Users()  # fetch user table
    data = request.form  # get the body data from the request
    # creating the user account on cognito api
    create_congnito_acc = Auth.SignUp(data['email'], data['password'])
    if not create_congnito_acc:  # if successful the result is required to be a dict
        return responseJSON(create_congnito_acc)

    # inserting the request body to the user table
    table.InsertToTable(User, data)

    return responseJSON('Data has been added successfully')


@app.route('/login', methods=['POST'])
def login():
    """
    Handles the user login and authentication.
    NOTE : it only accepts a POST Method
    :return: json
    """

    if not request.method == "POST":
        return responseJSON('Only POST method is allowed for this endpoint')

    user = request.form.to_dict()  # get data from request body
    email = user['email']
    password = user['password']
    User = table.Users()

    # search DB to check if email exist...(this part if optional).
    res = table.GetFromTable(User, email)
    if not isinstance(res, dict):  # if successful the result is required to be a dict
        return responseJSON('user does not exist')

    # Authenticating user email and password details in cognito API and
    # if successful returns an access token.
    if res := Auth.AuthenticateUser(email, password):
        return responseJSON(res)
    else:
        return responseJSON(res)


@app.route('/bank', methods=['POST'])
def bank():
    """
        Handles the user bank.
        it gets the token from the header and checks if it matches below criteria:
        1. if Authorization exist in the header
        2. if the Authorization value length is greater than 10
        3. verifies if the token gotten from the Authorization is correct, and it is not expired.
        4. checks if the instance of the response from the cognito API is dict
        5. it fetches user information with the access token from the AWS cognito
        6. if everything is okay, it writes to the user table with the request body using
            the email returned from the GetUser method and returns the data updated.

    :return: dict
    """
    if not request.method == "POST":
        return responseJSON('Only POST method is allowed for this endpoint')

    headers = request.headers
    if "Authorization" not in headers:  # checks if the authorization exist on the header
        return responseJSON('Invalid Credentials')

    bearer = headers.get('Authorization')

    if len(bearer) < 10:  # checks if the authorization value length is greater than 10
        return responseJSON('Invalid Credentials')

    token = bearer.split()[1]  # splits the authorization value to return the token
    user = Auth.GetUser(token)  # authenticates the token in cognito to return the user information

    if not isinstance(user, dict):
        return responseJSON(user)

    data = request.form.to_dict()  # converts the request body form data to dict
    User = table.Users()  # fetch user table
    user_email = Auth.fetchEmail(user)  # loops through the data returned from the GetUser method to return the  email

    keys = [{key: {'Value': data[key], 'Action': 'PUT'}} for key in data]
    Table.UpdateToTable(User, user_email, keys)  # updating data into the user table using the email

    return responseJSON(data)


