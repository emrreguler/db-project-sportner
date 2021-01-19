from flask import current_app, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from flask_login import current_user, login_user, login_required, logout_user
import psycopg2 
from markupsafe import escape
from userClass import User
from userClass import getUser
from passlib.hash import pbkdf2_sha256 as hasher
from datetime import date
import numpy as np

def home_page():
    today=datetime.today()
    day_name=today.strftime("%A")
    return render_template("home.html",day=day_name)

def index_page():
    if 'email' in session:
        return redirect(url_for('home_page'))
    return redirect(url_for('login_page'))

@login_required
def logout_page():
    # remove the username from the session if it's there
    flash(current_user.username)
    logout_user()
    session.pop('email', None)
    return render_template("logout.html") 

def login_page():
    if request.method == 'POST':
        try:
            connection = psycopg2.connect(user="postgres",
                                    password="191919",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="postgres")

            cursor = connection.cursor()
            cursor.execute("SELECT email, userid, usrpassword FROM users")
            user= cursor.fetchall()
            form_title=request.form['email']
            form_title1=request.form['password']
            for name in user:
                if(name[0]==form_title):
                    if(hasher.verify(form_title1,name[2])):
                        session['email'] = form_title
                        users=getUser(name[1])
                        login_user(users)
                        return redirect(url_for('home_page'))
            flash('User is not found')
            connection.commit() 
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    return render_template("login.html") 

def user_add_page():
    try:
        connection= psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        
        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("signup.html")
        else:
            form_title1 = request.form["username"]
            form_title2 = request.form["surname"]
            form_title3 = request.form["email"]
            form_title4 = hasher.hash(request.form["password"])
            form_title5 = request.form["age"]
            form_title6 = request.form["country"]
            form_title7 = request.form["proficiency"]
            form_title8 = request.form["city"]
            form_title9 = request.form["district"] 
            place_query=""" SELECT district FROM location WHERE district=%s"""
            cursor.execute(place_query,(form_title9,))
            place= cursor.fetchone()
            if(place==None):
                select_query=""" SELECT MAX(locationid) FROM location"""
                cursor.execute(select_query)
                maxlocid= cursor.fetchone()
                maxlocidint=maxlocid[0]
                insert_query = """ INSERT INTO location (locationid, country, city, district) VALUES (%s, %s, %s, %s)"""
                loc_tuple=(maxlocidint+1,form_title6,form_title8,form_title9)
                cursor.execute(insert_query, loc_tuple)
            select1_query= """ SELECT locationid FROM location WHERE district=%s"""
            cursor.execute(select1_query, (form_title9,))
            loc=cursor.fetchone()   
            locint=loc[0]
            select_query=""" SELECT MAX(userid) FROM users"""
            cursor.execute(select_query)
            maxuserid= cursor.fetchone()
            if maxuserid[0]==None:
                maxuseridint=0
            else:    
                maxuseridint=maxuserid[0]
            insert_query = """ INSERT INTO users (userid, locationid, username, surname, age, email, usrpassword, rate, proficiency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            item_tuple=(maxuseridint+1, locint, form_title1, form_title2, form_title5, form_title3, form_title4, 0, form_title7)
            cursor.execute(insert_query,item_tuple)
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")         
    return redirect(url_for("login_page")) 


@login_required
def sports_page():
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

        cursor = connection.cursor()
        cursor.execute("SELECT sportsid, sportname, isteam FROM sports")
        sport= cursor.fetchall()
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return render_template("sports.html",sport=sorted(sport))

@login_required
def posts_page(sportid):
    post=''
    try:
        connection = psycopg2.connect(user="postgres",
                                password="191919",
                                host="127.0.0.1",
                                port="5432",
                                database="postgres")
        cursor = connection.cursor()
        post_query="""SELECT postid, userid, postdate, title, description, sportsid, username FROM posts NATURAL RIGHT JOIN users WHERE sportsid=%s """
        #post_query="""SELECT * FROM posts WHERE sportsid=%s"""
        cursor.execute(post_query,(sportid,))
        post= cursor.fetchall()
        if post[0][2]==None:
            post=None
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return render_template("posts.html",post=post,sportnumtemp=sportid)


@login_required
def sportsplace_page():
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        #comment_query="""SELECT sportplaceid, locationid, sportsid, placename, rate, sportname FROM sportplace NATURAL RIGHT JOIN sports """
        #cursor.execute("SELECT sportplaceid, locationid, sportsid, placename, rate FROM sportplace")
        cursor.execute("SELECT sportplaceid, locationid, sportsid, placename, rate, sportname FROM sportplace NATURAL RIGHT JOIN sports WHERE placename IS NOT NULL")
        sportplace= cursor.fetchall()
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return render_template("sportplace.html",sportplace=sportplace) 

@login_required
def sportplace_add_page():
    try:
        connection= psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("sportplace_edit.html")
        else:
            form_title1 = request.form["country"]
            form_title2 = request.form["city"]
            form_title3 = request.form["district"]
            form_title4 = request.form["name"]
            form_title5 = request.form["sport"]
            sport_query=""" SELECT sportname FROM sports WHERE sportname=%s"""
            cursor.execute(sport_query,(form_title5,))
            sport= cursor.fetchone()
            if(sport==None):
                select2_query=""" SELECT MAX(sportsid) FROM sports"""
                cursor.execute(select2_query)
                maxsportid= cursor.fetchone()
                maxsportidint=maxsportid[0]
                insert2_query = """ INSERT INTO sports (sportsid, sportname, isteam) VALUES (%s, %s, %s, %s)"""
                sport_tuple=(maxsportidint+1,form_title5,True)
                cursor.execute(insert2_query, sport_tuple)
            place_query=""" SELECT district FROM location WHERE district=%s"""
            cursor.execute(place_query,(form_title3,))
            place= cursor.fetchone()
            if(place==None):
                select_query=""" SELECT MAX(locationid) FROM location"""
                cursor.execute(select_query)
                maxlocid= cursor.fetchone()
                maxlocidint=maxlocid[0]
                insert_query = """ INSERT INTO location (locationid, country, city, district) VALUES (%s, %s, %s, %s)"""
                loc_tuple=(maxlocidint+1,form_title1,form_title2,form_title3)
                cursor.execute(insert_query, loc_tuple)
            select1_query= """ SELECT locationid FROM location WHERE district=%s"""
            cursor.execute(select1_query, (form_title3,))
            loc=cursor.fetchone()   
            locint=loc[0]
            select3_query= """ SELECT sportsid FROM sports WHERE sportname=%s"""
            cursor.execute(select3_query, (form_title5,))
            sportid=cursor.fetchone()   
            sportidint=sportid[0]
            sportplace_query=""" SELECT MAX(sportplaceid) FROM sportplace"""
            cursor.execute(sportplace_query)
            maxplaceid= cursor.fetchone()
            maxplaceidint=maxplaceid[0]
            insert1_query = """ INSERT INTO sportplace (sportplaceid, locationid, sportsid, placename, rate) VALUES (%s, %s, %s, %s, %s)"""
            place_tuple=(maxplaceidint+1, locint, sportidint, form_title4, 0)
            cursor.execute(insert1_query,place_tuple)
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")         
    return redirect(url_for("sportsplace_page"))      

@login_required
def post_add_page(sportnum):
    usernum=current_user.get_id()
    today=date.today()
    try:
        connection= psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        
        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("post_edit.html")
        else:
            form_title1 = request.form["title"]
            form_title2 = request.form["description"]
            select_query=""" SELECT MAX(postid) FROM posts"""
            cursor.execute(select_query)
            maxpostid= cursor.fetchone()
            if maxpostid[0]==None:
                maxpostidint=0
            else:    
                maxpostidint=maxpostid[0]
            insert_query = """ INSERT INTO posts (postid, userid, postdate, title, description, sportsid, eqtoolid) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            item_tuple=(maxpostidint+1,usernum,today.strftime("%B %d, %Y"),form_title1,form_title2,sportnum, None)
            cursor.execute(insert_query,item_tuple)
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")         
    return redirect(url_for("posts_page",sportid=sportnum)) 

@login_required
def comment_page(postnum):
    comment=' '
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

        cursor = connection.cursor()
        comment_query="""SELECT commentid, userid, postid, commentdate, description, username FROM comment NATURAL RIGHT JOIN users WHERE postid=%s """
        #comment_query="""SELECT * FROM comment WHERE postid=%s"""
        cursor.execute(comment_query,(postnum,))
        comment= cursor.fetchall()
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return render_template("comment.html",comment=sorted(comment),postnumtemp=postnum)   

@login_required
def comment_add_page(postsid):
    usernum=current_user.get_id()
    today=date.today()
    try:
        connection= psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("comment_edit.html")
        else:
            form_title1 = request.form["description"]
            select_query=""" SELECT MAX(commentid) FROM comment"""
            cursor.execute(select_query)
            maxcomid= cursor.fetchone()
            if maxcomid[0]==None:
                maxcomidint=0
            else:    
                maxcomidint=maxcomid[0]
            insert_query = """ INSERT INTO comment (commentid, userid, postid, commentdate, description) VALUES (%s, %s, %s, %s, %s)"""
            item_tuple=(maxcomidint+1, usernum, postsid, today.strftime("%B %d, %Y"), form_title1)
            cursor.execute(insert_query,item_tuple)
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect(url_for("comment_page",postnum=postsid))    

@login_required
def eqtools_page():
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        cursor.execute("SELECT eqtoolid, eqtoolname, issale, isshared FROM equipmenttool")
        eqtool= cursor.fetchall()
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return render_template("eqtools.html",eqtool=sorted(eqtool)) 

@login_required
def delete_posts(postId, sportId):
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        post_query="""DELETE FROM posts WHERE postid=%s"""
        cursor.execute(post_query,(postId,))
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect(url_for("posts_page",sportid=sportId))  

@login_required
def delete_comments(postID, commentId):
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        post_query="""DELETE FROM comment WHERE commentid=%s"""
        cursor.execute(post_query,(commentId,))
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect(url_for("comment_page",postnum=postID)) 

@login_required
def delete_user():
    usernum=current_user.get_id()
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        user_query="""DELETE FROM users WHERE userid=%s"""
        cursor.execute(user_query,(usernum,))
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect(url_for("home_page")) 

@login_required
def update_user():
    usernum=current_user.get_id()
    try:
        connection= psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        
        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("update.html")
        else:
            form_title1 = request.form["username"]
            form_title2 = request.form["surname"]
            form_title3 = request.form["email"]
            form_title4 = hasher.hash(request.form["password"])
            form_title5 = request.form["age"]
            form_title6 = request.form["country"]
            form_title7 = request.form["proficiency"] 
            form_title8 = request.form["city"]
            form_title9 = request.form["district"] 
            place_query=""" SELECT district FROM location WHERE district=%s"""
            cursor.execute(place_query,(form_title9,))
            place= cursor.fetchone()
            if(place==None):
                select_query=""" SELECT MAX(locationid) FROM location"""
                cursor.execute(select_query)
                maxlocid= cursor.fetchone()
                maxlocidint=maxlocid[0]
                insert_query = """ INSERT INTO location (locationid, country, city, district) VALUES (%s, %s, %s, %s)"""
                loc_tuple=(maxlocidint+1,form_title6,form_title8,form_title9)
                cursor.execute(insert_query, loc_tuple)
            select1_query= """ SELECT locationid FROM location WHERE district=%s"""
            cursor.execute(select1_query, (form_title9,))
            loc=cursor.fetchone()   
            locint=loc[0]
            update_query = """ UPDATE users SET locationid=%s, username=%s, surname=%s, age=%s, email=%s, usrpassword=%s, rate=%s, proficiency=%s WHERE userid=%s"""
            update_tuple=(locint, form_title1, form_title2, form_title5, form_title3, form_title4, 0, form_title7, usernum)
            cursor.execute(update_query, update_tuple)
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")         
    return redirect(url_for("home_page"))  

@login_required
def users_page():
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        cursor.execute("SELECT username, surname, age, proficiency, rate, userid FROM users")
        users= cursor.fetchall()
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return render_template("users.html", users=users)      

@login_required
def rate_page(useriD):
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("rate.html")
        else:    
            user_query="""SELECT FROM users WHERE userid=%s"""
            cursor.execute(user_query,(useriD,))
            form_title=request.form["rate"]
            rate_query= """UPDATE users SET rate=%s WHERE userid=%s """
            rate_tuple=(form_title,useriD)
            cursor.execute(rate_query, rate_tuple)
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect(url_for("users_page"))

@login_required
def rate_sportplace_page(placeid):
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("rate.html")
        else:    
            #sportplace_query="""SELECT FROM sportplace WHERE sportplaceid=%s"""
            #cursor.execute(sportplace_query,(placeid,))
            form_title=request.form["rate"]
            rate_query= """UPDATE sportplace SET rate=%s WHERE sportplaceid=%s """
            rate_tuple=(form_title,placeid)
            cursor.execute(rate_query, rate_tuple)
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect(url_for("sportsplace_page"))

@login_required
def eqtool_add_page(eqtoolnum):
    usernum=current_user.get_id()
    today=date.today()
    try:
        connection= psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        
        cursor = connection.cursor()
        if request.method == "GET":
            return render_template("eqtool_post.html")
        else:
            form_title1 = request.form["title"]
            form_title2 = request.form["description"]
            form_title3 = request.form["share"]
            select_query=""" SELECT MAX(postid) FROM posts"""
            cursor.execute(select_query)
            maxpostid= cursor.fetchone()
            if maxpostid[0]==None:
                maxpostidint=0
            else:    
                maxpostidint=maxpostid[0]
            insert_query = """ INSERT INTO posts (postid, userid, postdate, title, description, sportsid, eqtoolid) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            item_tuple=(maxpostidint+1,usernum,today.strftime("%B %d, %Y"),form_title1,form_title2,None, eqtoolnum)
            cursor.execute(insert_query,item_tuple)
            insert1_query = """ UPDATE equipmenttool SET issale=%s, isshared=%s WHERE eqtoolid=%s"""
            if form_title3=='share':
                item1_tuple=(False, True, eqtoolnum)
                cursor.execute(insert1_query,item1_tuple)
            elif form_title3=='sale':
                item1_tuple=(True, False, eqtoolnum)
                cursor.execute(insert1_query,item1_tuple)
            """insert2_query = """ "SELECT issale FROM equipmenttool WHERE eqtoolid=%s""""
            cursor.execute(insert2_query,(eqtoolnum,))
            status=cursor.fetchone()"""
            connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")         
    return redirect(url_for("post_eqtool_page",eqtooliD=eqtoolnum))

@login_required
def post_eqtool_page(eqtooliD):
    post=''
    try:
        connection = psycopg2.connect(user="postgres",
                                password="191919",
                                host="127.0.0.1",
                                port="5432",
                                database="postgres")
        cursor = connection.cursor()
        join_query="""SELECT issale, isshared, postdate, title, description, userid, postid, eqtoolid, username FROM posts NATURAL RIGHT JOIN equipmenttool NATURAL JOIN users WHERE sportsid is NULL AND eqtoolid=%s """
        cursor.execute(join_query, (eqtooliD,))
        post= cursor.fetchall()
        if post[0][3]==None:
            post=None
        #post_query="""SELECT * FROM posts WHERE eqtoolid=%s"""
        #cursor.execute(post_query,(eqtooliD,))
        #post= cursor.fetchall()
        #print(post)
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return render_template("eqtool_edit.html",post=post,eqtoolnumtemp=eqtooliD)  

@login_required
def delete_eqtool(postId, eqtoolId):
    try:
        connection = psycopg2.connect(user="postgres",
                                  password="191919",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        cursor = connection.cursor()
        post_query="""DELETE FROM posts WHERE postid=%s"""
        cursor.execute(post_query,(postId,))
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return redirect(url_for("post_eqtool_page",eqtooliD=eqtoolId)) 
