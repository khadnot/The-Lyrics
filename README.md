# Don't Forget The Lyrics

Here is my web application based on the popular game show Don't Forget the Lyrics. You'll choose one of two songs from eight different music categories and try to fill in the missing lyrics. For the best score quickly and accurately complete the lyrics. 

## Heroku

To play the game click here: [Don't Forget The Lyrics!](https://dont-forget-the-lyrics.herokuapp.com/)

## Gameplay

Upon signing up for an account or logging into an existing account you'll be taken to the Genres page where you'll choose from either Hip Hop, Pop, Country, Rock, Dance, Latin, R&B, or Disney. Within each genre category will be the choice between two random songs. Once a song is chosen you'll have one minute to correctly guess the missing lyrics from the song. The faster you guess, the more points you'll receive. After completing all 8 genres if you scored at least 38,000 points you will get access to a bonus level.

## API used

I used the Musixmatch API (https://developer.musixmatch.com) to create my app. A free API Key is needed to clone app.

## Installation

Use the package manager pip to install requirements.txt.

```bash
pip install -r requirements.txt 
```  
Import DatabaseSongs.csv to create database of songs.

```bash
COPY songs(song_artist, song_name, song_id, genre_id)
FROM '\DatabaseSongs.csv'
DELIMITER ','
CSV HEADER;
```

## Tech Stack Used

**Backend** - Python, Flask, Axios, WTForms, SQLAlchemy  
**Frontend** - JavaScript, Jinja, Bootstrap, CSS
