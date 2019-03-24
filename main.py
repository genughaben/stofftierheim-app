import os, sys
from functools import wraps
from flask import request, Response, Flask, redirect, render_template as render
## ** ##
#
# This is the highly appreciated software code of the Stofftierheim Company (TM).
#
## ** ##

app = Flask(__name__)

account_name = os.getenv('NEXTCLOUD_USERNAME')
account_key = os.getenv('NEXTCLOUD_PASSWORD')
account_path = os.getenv('NEXTCLOUD_PATH')

stofftierheim_login = os.getenv('STOFFTIERHEIM_LOGIN')
stofftierheim_password = os.getenv('STOFFTIERHEIM_PASSWORD')

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ""+stofftierheim_login and password == ""+stofftierheim_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render('home.html')

@app.route('/secret_page')
@requires_auth
def secret_page():
    local_path = os.getcwd()
    file_name="test"
    image_date = "2019-01-01"
       
    return render(
       'secret_page.html',
        file_name=file_name,
        image_date=image_date,
        next_image_path='fehlt noch',
        previous_image_path='fehlt noch',
        newest_image_path='fehlt noch'
    )

if __name__ == "__main__":
   app.run()
