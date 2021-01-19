from flask import Flask, render_template, session, redirect, url_for, request
import view
from markupsafe import escape
from flask_login import LoginManager
from flask_login import current_user
from userClass import getUser
from userClass import User

import psycopg2 


login_manager = LoginManager()
@login_manager.user_loader
def load_user(userid):
    return getUser(userid)


def create_app():
    app = Flask(__name__)

    login_manager.init_app(app)
    login_manager.login_view="home_page"
    app.config["DEBUG"]=True
    app.config.from_object("settings")
    app.config['TESTING'] = False
   
    app.add_url_rule("/signup", view_func=view.user_add_page, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=view.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=view.logout_page, methods=["GET", "POST"])
    
    app.add_url_rule("/",view_func=view.index_page, methods=["GET", "POST"])
    app.add_url_rule("/home",view_func=view.home_page)
    app.add_url_rule("/home/delete-user",view_func=view.delete_user)
    app.add_url_rule("/home/update-user",view_func=view.update_user, methods=["GET", "POST"])
    app.add_url_rule("/home/users",view_func=view.users_page)
    app.add_url_rule("/home/users/<useriD>rate-user",view_func=view.rate_page, methods=["GET", "POST"])

    
    app.add_url_rule("/sports",view_func=view.sports_page)
    app.add_url_rule("/sportsplace",view_func=view.sportsplace_page)
    app.add_url_rule("/sportsplace/<placeid>rate-place",view_func=view.rate_sportplace_page, methods=["GET", "POST"])
    app.add_url_rule("/sportsplace/add-place",view_func=view.sportplace_add_page, methods=["GET", "POST"])
    app.add_url_rule("/sports/<sportid>posts",view_func=view.posts_page)
    app.add_url_rule("/sports/posts<sportId>/<postId>delete-post",view_func=view.delete_posts)
    app.add_url_rule("/sports/posts/<sportnum>new-post",view_func=view.post_add_page, methods=["GET","POST"])
    app.add_url_rule("/sports/posts/<postnum>comment",view_func=view.comment_page)
    app.add_url_rule("/sports/posts/comment<postID>/<commentId>delete-comment",view_func=view.delete_comments)
    app.add_url_rule("/sports/posts/comment/<postsid>new-comment",view_func=view.comment_add_page, methods=["GET","POST"])
    app.add_url_rule("/eqtool",view_func=view.eqtools_page)
    app.add_url_rule("/eqtool/<eqtooliD>posteqtool",view_func=view.post_eqtool_page)
    app.add_url_rule("/eqtool/posteqtool/<eqtoolnum>new-eqtool",view_func=view.eqtool_add_page, methods=["GET","POST"])
    app.add_url_rule("/eqtool/posteqtool<eqtoolId>/<postId>delete-eqtool",view_func=view.delete_eqtool)
   

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    return app

@login_manager.user_loader
def user_loader(userid):
    tempUser=None
    try:
        connection = psycopg2.connect(user="postgres",
                                password="191919",
                                host="127.0.0.1",
                                port="5432",
                                database="postgres")

        cursor = connection.cursor()
        user_query="""SELECT * FROM users WHERE userid=%s"""
        cursor.execute(user_query,(userid,))
        temp = cursor.fetchone()
        tempUser = User(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8])
        connection.commit() 
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    return tempUser

    

if __name__ == "__main__":
    app=create_app()
    app.run(host="127.0.0.1", port=8080)


