import os, sys
from functools import wraps
from flask import request, Response, Flask, redirect, render_template as render
from azure.storage.blob import BlockBlobService

## ** ##
#
# This is the highly appreciated software code of the Stofftierheim Company (TM).
#
## ** ##

app = Flask(__name__)

account_name = os.getenv('AZURE_ACCOUNT_NAME')
account_key = os.getenv('AZURE_ACCOUNT_KEY')
container_name = 'genughabenpi'

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

def get_blob_list(block_blob_service):
    generator = block_blob_service.list_blobs(container_name)
    blob_names = []
    dates = []
    for blob in generator:
        blob_names.append(blob.name)
        dates.append(blob.properties.properties.last_modified)
    return blob_names, dates

def get_newest_file(block_blob_service):
    generator = block_blob_service.list_blobs(container_name)
    return generator.items.pop()

@app.route('/image_list')
@requires_auth
def image_list():
    block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)
    blob_list, dates = get_blob_list(block_blob_service)
    return render('image_list.html', image_list=blob_list, dates=dates)

@app.route('/secret_page')
@requires_auth
def secret_page():
    block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)
    local_path = os.getcwd()
    file = get_newest_file(block_blob_service)
    file_fullname = file.name
    file_date = file.properties.last_modified.strftime("%Y-%m-%d")
    file_name = os.path.splitext(file_fullname)[0]
    full_path_to_file = os.path.join(local_path, 'static/images/'+file_name+'.jpg')
    if os.path.isfile(full_path_to_file):
        os.remove(full_path_to_file)

    block_blob_service.get_blob_to_path(container_name, file_fullname, full_path_to_file)

    return render(
        'secret_page.html',
        file_name=file_name,
        image_date=file_date,
        next_image_path='fehlt noch',
        previous_image_path='fehlt noch',
        newest_image_path='fehlt noch'
    )

if __name__ == "__main__":
   app.run()
