from google.cloud import storage
from flask import Flask, render_template, request, abort, jsonify

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

@app.route('/profiles')
def profiles():
    user = "Hervin"
    profiles = [
        {
            'site' : 'Snapchat',
            'code' : '...'
        },
        {
            'site' : 'LinkedIn',
            'code' : '...'
        }
    ]
    return render_template('profiles.html', user = user, profiles = profiles)

#@app.route('/login', methods=['GET','POST'])
#def login():
#    form = LoginForm()


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


@app.route('/dangerzone')
def dangerzone():
    return render_template('login_dangerzone.html')

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
    blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')
    #success: user created without problems
    return jsonify(success=True)

@app.route('/user/<username>/url/<url>', methods=['POST'])
def addUrl(username, url):
    # Make sure we have an url in the request
    if not url or not username:
        
        pass
    
    # turn url to qrcode img

    # add url/qrcode img to user
    pass

@app.route('/user/<username>/qr', methods=['POST'])
def addQr(username): 
    # Make sure we have an file in the request
    img = request.file.get('url', None)

    if not img or not username:
        #fail
        pass
    
    # turn img to url

    # turn url to qrcode img

    # add url/img to user
    pass
