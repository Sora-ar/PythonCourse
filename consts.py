import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

HEADERS = {
    'accept': os.getenv('ACCEPT'),
    'Authorization': os.getenv('AUTHORIZATION')
}
URL = 'https://api.themoviedb.org/3/discover/movie?include_adult=' \
      'false&include_video=false&sort_by=popularity.desc&page={}'
FIELDS = ['Title', 'Popularity', 'Score', 'Last day in cinema']
TITLE = 'title'
POPULARITY = 'popularity'
GENRE_IDS = 'genre_ids'
VOTE_AVERAGE = 'vote_average'
OVERVIEW = 'overview'
RELEASE_DATE = 'release_date'
SCORE = 'Score'
DATA_FORMAT = '%Y-%m-%d'
FILE_WITH_FILMS = 'film_file.csv'
