import psycopg2
import select
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def connect_db(instance,database):
        try:
            dsn = "dbname={dbname} user={dbuser} host={host} password={password}".format(dbname=database, dbuser='dbuser', host=instance, password='123')
            print (dsn)
            conn = psycopg2.connect(dsn)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            return conn
        except:
            print ("I am unable to connect to the database")



def dblisten(conn, channel):
    """
    Open a db connection and add notifications to *q*.
    """

    cur = conn.cursor()
    cur.execute('LISTEN {0}'.format(channel))
    print ("Waiting for notifications on channel {0}".format(channel))
    while 1:
        if select.select([conn],[],[],60) == ([],[],[]):
            pass
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                return notify



connection = connect_db('192.168.1.21','dbuser')
notify = dblisten(connection,'data')

print ("Got NOTIFY:", notify.pid, notify.channel, notify.payload)

if (notify.payload == 'admin login'):
    print ("Admin login detected")
