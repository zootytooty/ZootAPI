"""Class to control CRUD venue handling functionality."""

import pymongo


class VenueManagement:
    """To manage getting and adding gigs."""
    def __init__(
        self: object,
        username: str,
        password: str,
        connection_string: str,
        database: str,
    ):
        """Sets up the class & connects to the DB.

        Args:
            username (str): MongoDB Username
            password (str): MongoDB Password
            connection_string (str): Parameterised conn string, with accomodation for PW & UN
            database (str): Mongo DB name to use
        """
        self.conn = self.db_conn(
            username=username,
            password=password,
            connection_string=connection_string,
            database=database,
        )

    @staticmethod
    def db_conn(
        username: str,
        password: str,
        connection_string: str,
        database: str,
    ) -> pymongo.database.Database:
        """Creates MongoDB database connection.

        Args:
            username (str): DB Username
            password (str): DB Password
            connection_string (str): URI Connection String
            database (str): Database name to connect to

        Returns:
            pymongo.database.Database: Instantiated MongoDB object
        """
        connection_string = connection_string.format(
            username=username, password=password
        )

        client = pymongo.MongoClient(connection_string)
        return client.get_database(database)

    def get_venues(self: object):
        """Sources venues & their details.

        Returns:
            list: list of venues
        """
        filters = {}
        projection = {"_id": 0}
        return [x for x in self.conn.venues.find(filters, projection)]
