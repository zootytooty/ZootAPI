"""Class to control CRUD gig handling functionality."""

import datetime

import pymongo


class GigManagement:
    def __init__(
        self: object,
        username: str,
        password: str,
        connection_string: str,
        database: str,
    ):
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

    def get_gigs(self: object, filters: dict = {}):
        """Sources gigs & their details.

        TO-DO: Add default date filter

        Args:
            filters (dict, optional): Defaults to {}.
                                      Items to filter by such as venue, date or artists

        Returns:
            list: list of gigs
        """
        return [self.gig_prepper(gig) for gig in self.conn.gigs.find(filters)]

    def add_gigs(self: object, values: list) -> dict:
        """Method to insert one or many gigs into the database.
        Performs an upsert, based on the following premise:
            - Assume that if the date, venue, start time & price match then it's the same gig
            - If they match then update the gig. Possibly for the title or description changed
            - Hopefully this removes the presence of duplicates

        Args:
            self (object): GigManagement Class
            values (list): The gigs to insert

        Returns:
            dict: Metadata regarding the insert attempt, containing:
                    - Records attempted
                    - Existing records updated
                    - New records inserted
        """
        # Upsert new gigs into the DB
        upserted_gigs = [
            self.conn.gigs.update(self.create_filter(gig), gig, upsert=True)
            for gig in values
        ]

        return self.extract_upsert_metadata(upserted_gigs)

    @staticmethod
    def extract_upsert_metadata(attempts: list) -> dict:
        """Collects desired metadata from the attempted upserts.

        Args:
            attempts (list): Upsert response objects from mongodb

        Returns:
            dict: Metadata regarding the insert attempt, containing:
                    - Records attempted
                    - Existing records updated
                    - New records inserted
        """
        attempted = len(attempts)
        updated = 0
        added = 0

        for attempt in attempts:
            if attempt["nModified"] > 0:
                updated += attempt["nModified"]
            else:
                added += 1

        return {
            "records_attempted": attempted,
            "records_updated": updated,
            "records_added": added,
        }

    @staticmethod
    def create_filter(
        gig: dict,
        match_attributes: list = ["venue", "performance_date", "music_starts", "price"],
    ) -> dict:
        """Subsets a gig object to just the desired elements required to "upsert" on

        Args:
            gig (dict): Standard gig object
            match_attributes (list, optional): Fields to subset to.
                Defaults to ["venue", "performance_date", "music_starts", "price"].

        Returns:
            dict: Subsetted gig object
        """
        return {x: v for x, v in gig.items() if x in match_attributes}

    def gig_prepper(self: object, gig: dict) -> dict:
        """Cleans up & standardises formatting of gigs prior to return

        Args:
            self (object): GigManagement Class
            gig (dict): Gig object and values

        Returns:
            dict: Standardised gig object
        """
        performance_date = None
        if gig["performance_date"]:
            try:
                performance_date = self.datetime_date_to_string(
                    gig["performance_date"], "%Y-%m-%d"
                )
            except Exception:
                pass

        doors_open = None
        if gig["doors_open"]:
            doors_open = self.format_time_string(gig["doors_open"], "%-I:%M %p")

        music_starts = None
        if gig["music_starts"]:
            music_starts = self.format_time_string(gig["music_starts"], "%-I:%M %p")

        price = None
        if gig["price"]:
            price = float(gig["price"])

        return {
            "title": gig["title"],
            "venue": gig["venue"],
            "description": gig["description"],
            "performance_date": performance_date,
            "doors_open": doors_open,
            "music_starts": music_starts,
            "price": price,
            "url": gig["url"],
            "image_url": gig["image_url"],
        }

    @staticmethod
    def format_time_string(string: str, format: str) -> str:
        """Converts a time string into the requested format.

        Args:
            string (str): Starting time string
            format (str): Desired time format

        Returns:
            str: Time reformatted into desired format
        """
        # Convert timestamp object
        try:
            dt = datetime.datetime.strptime(string, "%H:%M:%S")
        except Exception:
            dt = datetime.datetime.strptime(string, "%H:%M")

        # Reformat
        return dt.strftime(format)

    @staticmethod
    def datetime_date_to_string(date: datetime.date, format: str) -> str:
        """Converts a date string into the requested format.

        Args:
            date (datetime.date): Starting date object
            format (str): Desired date format

        Returns:
            str: Date reformatted into desired format
        """
        return date.strftime(format)
