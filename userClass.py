from flask import current_app
from flask_login import UserMixin
from flask_login import login_manager
from flask_login import login_required 
import psycopg2 
import numpy as np


class User(object):
    def __init__(self, userid, locationid, username, surname, age, email, usrpassword, rate, proficiency):
        self.userid = userid
        self.locationid = locationid
        self.username = username
        self.surname = surname
        self.age = age
        self.email = email
        self.usrpassword = usrpassword
        self.rate = rate
        self.proficiency = proficiency


        #if not PY2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        #    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.userid

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented


def getUser(userid):
    user=''
    try:
        connection = psycopg2.connect(user="postgres",
                                password="191919",
                                host="127.0.0.1",
                                port="5432",
                                database="postgres")

        cursor = connection.cursor()
        user_query="""SELECT userid, locationid, username, surname, age, email, usrpassword, rate, proficiency  FROM users WHERE userid=%s"""
        cursor.execute(user_query,(userid,))
        users= cursor.fetchall()
        userarr=np.array(users)
        user=User(userarr[0][0],userarr[0][1],userarr[0][2],userarr[0][3],userarr[0][4],userarr[0][5],userarr[0][6],userarr[0][7],userarr[0][8])
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    if(len(userarr) == 0):
        return None
    else:
        return user
