HEADERS = {
    'accept': 'application/json',
    'Authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNT"
                     "UyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMD"
                     "FmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW"
                     "9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
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
