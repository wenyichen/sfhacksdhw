from flask import Flask, render_template, request

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


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)