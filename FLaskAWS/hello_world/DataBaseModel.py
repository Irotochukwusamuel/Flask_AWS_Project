import json

import boto3


class Table:
    """
        This class manages the DYNAMODB CRUD using BOTO 3
    """

    def __init__(self):
        self.client = boto3.client('dynamodb')
        self.dynamodb = boto3.resource('dynamodb')

    def check_Table_exist(self, tablename):
        """
        This method accepts the parameter of the tablename and check if the table already exist on the DB and
        returns True or False.

        :param tablename: str
        :return: bool
        """
        tables = self.client.list_tables()
        Tablenames = tables['TableNames']
        if Tablenames and tablename in Tablenames:
            return True
        return False

    def Users(self):
        """
        This method sets the tablename as Users and checks if the table exist before creating a new
        table.

        Note : It sets the email as the hash key or primary key, and it attributes as string

        """

        __tablename__ = 'Users'
        if not self.check_Table_exist(__tablename__):
            # CHECKS IF THE TABLE EXIST, IF NOT, IT CREATES A NEW TABLE
            table = self.dynamodb.create_table(
                TableName=__tablename__,
                KeySchema=[
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'
                    },
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'email',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            table.wait_until_exists()
            return table

        return self.dynamodb.Table(__tablename__)

    @staticmethod
    def InsertToTable(tablename, data):
        """
        This method fetches the table using the table name and inserts data into it.

        :param tablename:
        :param data:
        :return: str
        """
        try:
            tablename.put_item(
                Item=data.to_dict()
            )
            return "Data has been inserted successfully"
        except Exception as e:
            return str(e)

    @staticmethod
    def GetFromTable(tablename, email):
        """
        This method fetches the table using the table name and searches for the email which is the hash key to return the
        designated data

        :param tablename:
        :param email:
        :return: dict
        """
        try:
            response = tablename.get_item(
                Key={"email": email}
            )
            item = response['Item']
            return item
        except Exception as e:
            return str(e)

    @staticmethod
    def UpdateToTable(tablename, email, data):
        """
        This method updates the table row with value using the email which is the hash key

        :param data: list of dict
        :param tablename:
        :param email: str
        :return: str
        """

        keys = {list(key.keys())[0]: key[value] for key in data for value in key}
        try:
            tablename.update_item(
                Key={
                    'email': email,
                },
                AttributeUpdates=keys
            )
        except Exception as e:
            return str(e)
