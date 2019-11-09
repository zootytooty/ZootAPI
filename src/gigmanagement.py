"""
Desc: 
"""
import os
# import yaml
import pymysql as mysql
import datetime


class GigManagement():

    def __init__(self):
        self.conn = self.db_conn()
        self.cursor = self.conn.cursor()


    def get_gigs(self, filters={}):
        """Sources gigs & their details

        TO-DO: Add default date filter
        
        Args:
            filters (dict, optional): Defaults to {}.
                                      Items to filter by such as venue, date or artists
    
        Returns:
            list: list of gigs
        """

        # Create base query & any additional filters
        sql = ["SELECT * FROM zootdb.gig_guide WHERE 1=1"]
        for param in filters:
            sql.append("AND {0} = %({0})s".format(param))

        # Execute
        self.cursor.execute(' '.join(sql), filters)
        return [self.gig_prepper(response) for response in self.cursor]


    def add_gigs(self, values):

        sql = """INSERT INTO zootdb.gig_guide (venue, title, music_starts, doors_open, performance_date, price, description, url, image_url) 
                 VALUES (%(venue)s, %(title)s, %(music_starts)s, %(doors_open)s, %(performance_date)s, %(price)s, %(description)s, %(url)s, %(image_url)s)"""

        self.cursor.executemany(sql, values)
        self.conn.commit()

        response = {
            "records_added": self.cursor.rowcount,
        }

        return response
    

    def db_conn(self):

        # Just for testing & setup purposes
        # conf = yaml.load(open('conf.yaml', 'r'))
        # rds = conf['rds']

        # hostname = rds['endpoint']
        # username = rds['master-user']
        # password = rds['master-password']
        # database = rds['database-name']
        
        hostname = os.environ['RDS_ENDPOINT']
        username = os.environ['RDS_MASTER_USER']
        password = os.environ['RDS_MASTER_PASSWORD']
        database = os.environ['RDS_DATABASE_NAME']

        conn = mysql.connect(host=hostname,
                             user=username, 
                             passwd=password, 
                             db=database,
                             cursorclass=mysql.cursors.DictCursor)

        return conn


    def gig_prepper(self, gig):

        performance_date = None
        if gig['performance_date']:
            performance_date =  self.datetime_date_to_string(gig['performance_date'], "%Y-%m-%d")

        doors_open = None
        if gig['doors_open']:
            doors_open =  self.timedelta_to_string(gig['doors_open'], "%-I:%M %p")

        music_starts = None
        if gig['music_starts']:
            music_starts =  self.timedelta_to_string(gig['music_starts'], "%-I:%M %p")

        price = None
        if gig['price']:
            price =  float(gig['price'])

        return {
            'title': gig['title'],
            'venue': gig['venue'],
            'description': gig['description'],
            'performance_date': performance_date,
            'doors_open': doors_open,
            'music_starts': music_starts,
            'price': price,
            'url': gig['url'],
            'image_url': gig['image_url']
            }


    def timedelta_to_string(self, time, format):
        return (datetime.datetime.min + time).strftime(format)

    def datetime_date_to_string(self, date, format):
        return date.strftime(format)


