"""Class to control CRUD venue handling functionality."""

from typing import List

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

    def get_venues(self: object) -> List[dict]:
        """Sources venues & their details.

        Returns:
            List[dict]: list of venues
        """
        filters = {}
        projection = {"_id": 0}
        return [x for x in self.conn.venues.find(filters, projection)]

    def add_venue(self: object, venue_details: dict) -> dict:
        """Method to insert one venue into the database.

        Performs a straight insert attempt

        Args:
            venue_details (list): The venue details to insert

        Returns:
            dict: Metadata regarding the insert attempt, containing:
                    - Records attempted
                    - Existing records updated
                    - New records inserted
        """
        inserted_venue = self.conn.venues.update(
            venue_details, venue_details, upsert=True
        )

        if inserted_venue["ok"] == 1:
            response = {
                "attempted": inserted_venue["n"],
                "already_existed": inserted_venue["updatedExisting"],
                "added": 1 if inserted_venue["updatedExisting"] is False else 0,
            }
        else:
            response = {"attempted": 0, "already_existed": False, "added": 0}

        return response
