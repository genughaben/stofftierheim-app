import os
import sys
from functools import wraps
from flask import request, Response, Flask, redirect, render_template as render
import easywebdav
from urllib.parse import urlparse
easywebdav.basestring = str
easywebdav.client.basestring = str

## ** ##
#
# This is the highly appreciated software code of the Stofftierheim Company (TM).
#
## ** ##

app = Flask(__name__)

account_name = os.getenv('NEXTCLOUD_USERNAME')
account_key = os.getenv('NEXTCLOUD_PASSWORD')
account_path = os.getenv('NEXTCLOUD_PATH_STOFF')

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
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


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


def get_youngest_file_from_nextcloud():
    easywebdav.basestring = str
    easywebdav.client.basestring = str
    parse_object = urlparse(account_path)
    domain = parse_object.netloc
    protocol = parse_object.scheme
    folder = parse_object.path

    webdav = easywebdav.connect(
        domain,
        username=account_name,
        password=account_key,
        protocol=protocol,
        port=443)

    files = webdav.ls(folder)

    from datetime import datetime
    file_and_date = {}
    for file in files:
        date_string = file.name.split('/')[-1].split('_image_')[0]
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d_%H-%M-%S")
            file_and_date[date] = file.name
        except:
            continue

    biggest_key = file_and_date.keys()

    os.environ['TZ'] = 'Europe/Amsterdam'
    now = datetime.now()
    youngest = max(dt for dt in file_and_date if dt < now)
    youngest_file_path = file_and_date[youngest]
    youngest_file_name = os.path.basename(youngest_file_path)
    local_youngest_file_name = './static/images/current/'+youngest_file_name
    webdav.download(youngest_file_path, local_youngest_file_name)
    return youngest_file_name, youngest.strftime('%Y-%m-%d %H:%M:%S')


@app.route('/secret_page')
@requires_auth
def secret_page():
    local_path = os.getcwd()
    [file_name, image_date] = get_youngest_file_from_nextcloud()
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
