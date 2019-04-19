"""
Desc: 
"""

import yaml
import pymysql as mysql


class GigManagement():

    def __init__(self, ):
        self.conn = self.db_conn()
        self.cursor = self.conn.cursor()


    def get_gigs(self, filters={}):
        """Sources gigs & their details

        TO-DO: Add default date filter
        
        
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
        return [response for response in self.cursor]


    def add_gig(self, venue, title, music_starts, doors_open, performance_date, price, description, url, image_url):

        sql = """
                INSERT INTO zootdb.gig_guide 
                    (venue, title, music_starts, doors_open, performance_date, price, description, url, image_url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        vals = (venue, title, music_starts, doors_open, performance_date, price, description, url, image_url)
        
        self.cursor.execute(sql, vals)
        self.conn.commit()

        self.cursor.execute('SELECT LAST_INSERT_ID()')
        gig_id = self.cursor.fetchone()

        return gig_id['LAST_INSERT_ID()']
    

    def db_conn(self):

        # Just for testing & setup purposes
        conf = yaml.load(open('conf.yaml', 'r'))
        rds = conf['rds']

        hostname = rds['endpoint']
        username = rds['master-user']
        password = rds['master-password']
        database = rds['database-name']

        conn = mysql.connect(host=hostname,
                             user=username, 
                             passwd=password, 
                             db=database,
                             cursorclass=mysql.cursors.DictCursor)

        return conn

