import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class Cognito:
    """
        This class manages the connection and management of users from the cognito API.

        NOTE: In this class the username parameter was substituted for email
    """

    def __init__(self):
        self.client_id = '5gdcl61lrfj0tuup7rmlb5tl7p'  # the user pool client id
        self.pool_id ='us-east-1_hPBikDQe1'  # the pool id
        self.client = boto3.client('cognito-idp', region_name='us-east-1')

    def SignUp(self, email, password):

        """
             Apply the set_email_verified and set_account_confirmed if you want to handle the
             email confirmation and setting the user Account Status to Confirmed which disables
             AWS from prompting the users to verify their email.

        """
        try:
            self.client.sign_up(ClientId=self.client_id, Username=email, Password=password)
            self.set_email_verified(email)  # set user email_verified as true
            self.set_account_confirmed(email, password)  # set account status as confirmed
            return True

        except Exception as e:
            return str(e)

    def set_email_verified(self, email):
        """
            This method sets the user account email verification as true.
            Use this method if you want to set a user email as true without prompting
            them to verify their email.

        :param email:
        :return: bool
        """
        self.client.admin_update_user_attributes(
            UserPoolId=self.pool_id,
            Username=email,
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ]
        )
        return True

    def set_account_confirmed(self, email, password):
        """
        This method sets the account status as CONFIRMED by setting the user password as permanent

        :param email:
        :param password:
        :return: bool
        """
        self.client.admin_set_user_password(
            UserPoolId=self.pool_id,
            Username=email,
            Password=password,
            Permanent=True
        )
        return True

    def AuthenticateUser(self, email, password):
        """
        This method initiates an authentication with the user email and password and return access token
        after auth was successful. Don't change the AuthFLow it uses the email as username and password
        for the validation. please reference to AWS BOTO3 INITIATE_AUTH for more information.

        :param email:
        :param password:
        :return: dict
        """
        try:
            res = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            return {
                "AccessToken": res['AuthenticationResult']['AccessToken'],
            }
        except Exception as e:
            return str(e)

    def GetUser(self, AccessToken):
        """
        This method returns the user information from the cognito pool
        using the user access token after login.

        :param AccessToken:
        :return: dict
        """
        try:
            res = self.client.get_user(
                AccessToken=AccessToken
            )
            return res
        except Exception as e:
            return str(e)

    @staticmethod
    def fetchEmail(data):
        """
        loops through the dictionary data returned from GetUser method and return the user email

        :param data: dict
        :return: str
        """
        for x in data['UserAttributes']:
            if x['Name'] == 'email':
                return str(x['Value'])

    """
        USE BELOW METHODS IF YOU WANT TO HANDLE THE USER AUTHENTICATION AND FORCE USERS  
        TO VERIFY THEIR EMAIL OR CHANGE USER PASSWORD
    """

    def SendToVerification(self, email):
        """
        This method send the confirmation code to the user email.

        :param email:
        """
        try:
            res = self.client.resend_confirmation_code(
                ClientId=self.client_id,
                Username=email
            )
            return res
        except Exception as e:
            return str(e)

    def VerifyEmail(self, email, code):
        """
        This method verifies the user confirmation code and email after the code has been sent their email

        :param email: str
        :param code: str
        """
        try:
            res = self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=code
            )
            return res
        except Exception as e:
            return str(e)

    def ForgotPassword(self, email):
        """
        This method sends a confirmation code to the user email for change of password

        :param email:
        """
        try:
            res = self.client.forgot_password(
                ClientId=self.client_id,
                Username=email
            )
            return res
        except Exception as e:
            return str(e)

    def ConfirmForgotPassword(self, email, code, new_password):
        """
        This method verifies the user confirmation code and email after the code has been sent their email
        and set the new password to their account

        :param new_password:
        :param email:
        :param code:
        """
        try:
            res = self.client.confirm_forgot_password(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=code,
                Password=new_password
            )
            return res
        except Exception as e:
            return str(e)

    def ChangePassword(self, AccessToken, old_password, new_password):
        """
        This method uses the user access token to change the user password to new password.
        NOTE : this method is applicable only when the user is already authenticated.

        :param AccessToken:
        :param old_password:
        :param new_password:
        """
        try:
            res = self.client.change_password(
                PreviousPassword=old_password,
                ProposedPassword=new_password,
                AccessToken=AccessToken
            )
            return res
        except Exception as e:
            return str(e)
