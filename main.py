from google.cloud import storage
from flask import Flask, render_template, request, abort, jsonify
import requests

PROJECT_NAME='sfhacksdhw'
BUCKET_NAME='sfhacksdhw.appspot.com'
app = Flask(__name__)
#login_manager = LoginManager()

#login_manager.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    user = 'Hello there'
    return render_template('index.html', user = user)

@app.route('/profiles/<username>')
def profiles(username):
    user = getUser(username)
    return render_template('profiles.html', profiles = user)

@app.route('/dangerzone')
def dangerzone():
    return render_template('login_dangerzone.html')
    
@app.route('/user/<username>', methods=['POST'])
def createUser(username):
    #if successful 200 else 500
    gcs_client = storage.Client(project=PROJECT_NAME)
    bucket = gcs_client.get_bucket(BUCKET_NAME)
    user_string = username + "/"
    blob = bucket.blob(user_string)
    if blob.exists():
        #fail
        abort(400)
    blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
    #success: user created without problems
    return jsonify(success=True)

@app.route('/user/<username>', methods=['GET'])
def getUser(username):
    #if successful 200 else 400
    gcs_client = storage.Client(project=PROJECT_NAME)
    bucket = gcs_client.get_bucket(BUCKET_NAME)
    user_string = username + "/"
    blob = bucket.blob(user_string)
    if not blob.exists():
        #fail
        abort(400)
    blobs = list(bucket.list_blobs(prefix=user_string))
    links = [jsonify(url=b.name, imgurl=b.generate_signed_url(86400)) for b in blobs]
    #success: user created without problems
    return jsonify(success=True,urls=links)

@app.route('/user/<username>/url/<url>', methods=['POST'])
def addUrl(username, url):
    # Make sure we have an url in the request
    if not url or not username:
        abort(400)
    gcs_client = storage.Client(project=PROJECT_NAME)
    bucket = gcs_client.get_bucket(BUCKET_NAME)
    user_string = username + "/"
    blob = bucket.blob(user_string)
    if not blob.exists():
        #fail
        abort(400)
    # if url already exists
    url_string = username + "/" + url
    blob = bucket.blob(url_string)
    if blob.exists():
        abort(400)

    # turn url to qrcode img
    img = requests.get("https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + url).content

    # add url/qrcode img to user
    blob.upload_from_file(img, content_type='PNG')
    return jsonify(success=True)

@app.route('/user/<username>/qr', methods=['POST'])
def addQr(username): 
    # Make sure we have an file in the request
    img = request.file.get('img', None)
    if not img or not username:
        abort(400)
    # turn img to url

    # turn url to qrcode img

    # add url/img to user
    pass
