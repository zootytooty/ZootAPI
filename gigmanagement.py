"""
Desc: 
"""

import yaml
import pymysql as mysql


class GigManagement():

    def __init__(self, ):
        self.conn = self.db_conn()
        self.cursor = self.conn.cursor()


    def get_gigs(self, venue):

        qry = """
              SELECT *
              FROM zootdb.gig_guide
              WHERE venue = %s
              """

        self.cursor.execute(qry, [venue])
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

