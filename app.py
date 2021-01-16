import os

from flask import Flask, render_template, request, redirect, session, flash, json, g, jsonify, Response
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql.expression import func
from flask_bcrypt import Bcrypt
import re
import random
import requests
from keys import api_key

from forms import AddUserForm, EditUserForm, LoginForm
from models import db, connect_db, User, Genre, Song

CURR_USER_KEY = "curr_user"
BASE_URL = 'https://api.musixmatch.com/ws/1.1/track.lyrics.get?format=json&track_id='

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
  os.environ.get('DATABASE_URL', 'postgres:///lyrics'))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "CH1LD15HG4MB1N0")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

bcrypt = Bcrypt()

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

  form = AddUserForm()

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

      do_login(user)
      flash(f"Hello, {user.first_name}!", "success")
      session['user_id'] = user.id
      session['username'] = user.username
      return redirect('/')

    except IntegrityError:
      flash("Username already taken", 'danger')
      return redirect('/signup')

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
      session['username'] = user.username
      return redirect('/')
    
    flash("Invalid credentials.", "danger")

  return render_template('users/login.html', form=form)

@app.route('/edit', methods=["GET", "POST"])
def edit_user():
  """Edit User Info"""

  if CURR_USER_KEY in session:

    form = EditUserForm()

    user = User.query.get(session[CURR_USER_KEY])

    if user:

      if form.validate_on_submit():

        user.username=form.username.data or user.username
        user.first_name=form.first_name.data or user.first_name
        user.last_name=form.last_name.data or user.last_name
        user.email=form.email.data or user.email

        password = form.password.data
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user.password=hashed_pwd

        db.session.commit()

        session['username'] = user.username

        flash("User Info Saved", "success")
        return redirect('/genres')

    else:
      flash("Please Login or Sign-up", "danger")
      return redirect('/login')

  else:
    flash("Please Login or Sign-up", "danger")
    return redirect('/login')

  return render_template('users/edit.html', form=form)

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

@app.route('/genres', methods=["GET", "POST"])
def get_genres():

  genres = Genre.query.all()

  return render_template('home.html', genres=genres)

@app.route('/genres/<string:genre>')
def get_songs(genre):

  songs = Song.query.join(Genre).filter(Genre.genre == f'{genre}').all()

  try:
    rand_songs = random.sample(list(songs), 2)
  except ValueError:
    rand_songs = Song.query.join(Genre).filter(Genre.genre == 'Bonus').first()

  if genre == 'Disney':
    return render_template(f'/genres/Disney.html', rand_songs=rand_songs, genre=genre)

  if genre == 'Bonus':
    return render_template(f'/genres/Bonus.html', rand_songs=rand_songs, genre=genre)

  return render_template(f'/genres/genre.html', rand_songs=rand_songs, genre=genre)

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
  line4 = lyrics.split('\n')[3]
  ghost = re.sub("[A-z]", '_', line4)

  return render_template('lyrics.html', line1=line1, line2=line2, 
                          line3=line3, line4=line4, ghost=ghost, song=song, genre=genre)

@app.route('/jsonres', methods=["POST"])
def jsonres():

  if CURR_USER_KEY in session:
    user = User.query.get(session[CURR_USER_KEY])

    response = request.json
    score = response['score']

    user.score = score
    db.session.commit()

    if score >= user.high_score:
      user.high_score = score
      db.session.commit()

    return jsonify({ 'score' : score })
  
  else:
    return jsonify({ 'score' : score })

  return jsonify({ 'score' : score })

@app.route('/game-over', methods=["GET", "POST"])
def game_over():

  if CURR_USER_KEY in session:
    user = User.query.get(session[CURR_USER_KEY])

    name = user.first_name

    score = user.score

    players = User.query.order_by(User.high_score.desc()).limit(5)

    pos = [*range(1, 6)]

    top_five = zip(pos, players)

    return render_template('endgame.html', name=name, score=score, top_five=top_five)

  return render_template('guestgame.html')