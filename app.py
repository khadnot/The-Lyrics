from flask import Flask, render_template, request, redirect, session, flash, json, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from  sqlalchemy.sql.expression import func
import re
import random
import requests
import string
from keys import api_key

from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Genre, Song

CURR_USER_KEY = "curr_user"
BASE_URL = 'https://api.musixmatch.com/ws/1.1/track.lyrics.get?format=json&track_id='

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lyrics'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "CH1LD15HG4MB1N0"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
  """If we're logged in, add curr user to Flask global."""

  if CURR_USER_KEY in session:
    g.user = User.query.get(session[CURR_USER_KEY])

  else:
    g.user = None

def do_login(user):
  """Log in user."""

  session[CURR_USER_KEY] = user.id

def do_logout():
  """Logout user."""

  if CURR_USER_KEY in session:
    del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
  """Handle user signup.

  Create new user and add user to database. Redirect to home page."""

  form = UserAddForm()

  if form.validate_on_submit():
    try:
      user = User.signup(
        username=form.username.data,
        password=form.password.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        email=form.email.data,
      )
      db.session.commit()

    except IntegrityError:
      flash("Username already taken", 'danger')
      return render_template('users/signup.html', form=form)

    do_login(user)

    return redirect('/')

  else:
    return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
  """Handle user login."""

  form = LoginForm()

  if form.validate_on_submit():
    user = User.authenticate(form.username.data,
                             form.password.data)

    if user:
      do_login(user)
      flash(f"Hello, {user.first_name}!", "success")
      session['user_id'] = user.id
      return redirect('/')
    
    flash("Invalid credentials.", "danger")

  return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
  """Handle user logout."""

  if CURR_USER_KEY in session:
    do_logout()
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/login')

@app.route('/')
def home_page():

  return render_template('title.html')

@app.route('/genres')
def get_genres():

  genres = Genre.query.all() # lists all the genres

  return render_template('home.html', genres=genres) # page with all the genres listed

# Work on this route. On genre click return songs from that genre.
@app.route('/genres/<string:genre>')
def get_songs(genre):

  songs = Song.query.join(Genre).filter(Genre.genre == f'{genre}').all()

  try:
    rand_songs = random.sample(list(songs), 2)
  except ValueError:
    rand_songs = Song.query.join(Genre).filter(Genre.genre == 'Bonus').first()

  return render_template(f'/genres/{genre}.html', rand_songs=rand_songs, genre=genre)

@app.route('/genres/<string:genre>/<int:song_id>')
def get_lyrics(genre, song_id):

  song = Song.query.filter_by(song_id=song_id).first()

  url = BASE_URL+f'{song_id}&apikey={api_key}'

  response = requests.get(url)
  data = json.loads(response.content)
  lyrics = data['message']['body']['lyrics']['lyrics_body']

  line1 = lyrics.split('\n')[0]
  line2 = lyrics.split('\n')[1]
  line3 = lyrics.split('\n')[2]
  ghost = re.sub("[A-z]", '_', line3)


  arr = []
  lyrics = line3.split(' ')
  lyrics = [''.join(c for c in s if c not in string.punctuation) for s in lyrics]
  for lyric in lyrics:
    arr.append(lyric)

  return render_template('lyrics.html', line1=line1, line2=line2, 
                          line3=line3, ghost=ghost, arr=arr, song=song, genre=genre)

'''
t_id = '13846989' # Around the World by Daft Punk
  #t_id_1 = '201234497' # WAP by Cardi B and Megan The Stallion
  #t_id_2 = '84684086' # Human Nature by Michael Jackson
  #t_id_3 = '99769120' # Ni**as in Paris by The Throne
  #t_id_4 = '86095153' # Day 'N' Nite by Kid Cudi

  url = BASE_URL+f'{t_id}&apikey={api_key}'

  response = requests.get(url)
  data = json.loads(response.content)
  lyrics = data['message']['body']['lyrics']['lyrics_body']

  line1 = lyrics.split('\n')[0]
  line2 = lyrics.split('\n')[1]
  line3 = lyrics.split('\n')[2]
  ghost = re.sub("[A-z]", '_', line3)


  arr = []
  lyrics = line3.split(' ')
  lyrics = [''.join(c for c in s if c not in string.punctuation) for s in lyrics]
  for lyric in lyrics:
    arr.append(lyric)

  return render_template('index.html', line1=line1, line2=line2, line3=line3, ghost=ghost, arr=arr)

'''