import requests
from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta
import csv
import pprint

headers = {
    'accept': 'application/json',
    'Authorization': "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNT"
                     "UyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMD"
                     "FmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW"
                     "9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
}


class Films:
    FIELDS = ['Title', 'Popularity', 'Score', 'Last day in cinema']

    def __init__(self, pages):
        self.data = []
        self.get_data(pages)
        self.pairs = []
        self.collection = []

    # 1. Fetch the data from desired amount of pages
    def get_data(self, pages):
        for i in range(1, pages + 1):
            url = f'https://api.themoviedb.org/3/discover/movie?include_adult=' \
                  f'false&include_video=false&sort_by=popularity.desc&page={i}'
            response = requests.get(url=url, headers=headers)
            self.data.extend(response.json()['results'])

    # 2. Give a user all data
    def get_all_data(self):
        return self.data

    # 3. All data about movies with indexes from 3 till 19 with step 4
    def slicing_data(self):
        return self.data[3:19:2]

    # 4. Name of the most popular title
    def get_most_popular_title(self):
        return max(self.data, key=lambda a: a['popularity'])['title']

    # 5. Names of titles which has in description key words which a user put as parameters
    def get_title_by_key_words(self):
        keywords = [f'{input("Find: ")}']
        return [film['title'] for film in self.data if any(keyword in film['overview'] for keyword in keywords)]

    # 6. Unique collection of present genres (the collection should not allow inserts)
    def get_unique_genres(self):
        return frozenset(genre for film in self.data for genre in film.get('genre_ids', []))

    # 7. Delete all movies with user provided genre
    def delete_movies(self):
        num_genre = input('Delete (number of genre): ')
        return list(filter(lambda film: num_genre not in film['genre_ids'], self.data))

    # 8. Names of most popular genres with numbers of time the appear in the data
    def get_most_popular_genres(self):
        return dict(Counter(genre for film in self.data for genre in film['genre_ids']).most_common())

    # 9. Collection of film titles  grouped in pairs by common genres (the groups should not allow inserts)
    def get_titles_grouped(self):
        for first_film in self.data:
            for second_film in self.data:
                if first_film['title'] != second_film['title'] and set(first_film['genre_ids']).intersection(
                        second_film['genre_ids']):
                    self.pairs = [(first_film['title'], second_film['title'])]
                    return self.pairs

    # 10. Return initial data and copy of initial data where first id in list of film genres was replaced with 22
    def get_copy_data_with_new_id(self):
        copy_data = deepcopy(self.data)
        for i in copy_data:
            i['genre_ids'][0] = 22
        return self.data, copy_data

    # 11. Collection of structures with part of initial data which has the following fields:
    #   •	Title
    #   •	Popularity (with 1 decimal point with maximum precision)
    #   •	Score (vote_average without fractional part)
    #   •	Last_day_in_cinema (2 months and 2 weeks after the release_date)
    #   Collection should be sorted by score and popularity
    def get_collection_with_data(self):
        for film in self.data:
            structures = {
                'Title': film['title'],
                'Popularity': round(film['popularity'], 1),
                'Score': int(film['vote_average']),
                'Last day in cinema': (datetime.strptime(film['release_date'], '%Y-%m-%d') +
                                       timedelta(weeks=8, days=4)).strftime('%Y-%m-%d')
            }
            self.collection.append(structures)
        self.collection.sort(key=lambda f: (f['Score'], f['Popularity']))
        return self.collection

    # 12. Write information from previous step to a csv file using path provided by user
    def write_data_in_csv(self):
        with open('film_file.csv', mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, self.FIELDS)
            writer.writeheader()
            writer.writerows(self.collection)


x = Films(3)

# 2
pprint.pprint(x.get_all_data())

# # 3
# pprint.pprint(x.slicing_data())

# # 4
# pprint.pprint(x.get_most_popular_title())

# # 5
# pprint.pprint(x.get_title_by_key_words())

# # 6
# pprint.pprint(x.get_unique_genres())

# # 7
# pprint.pprint(x.delete_movies())

# # 8
# pprint.pprint(x.get_most_popular_genres())

# # 9
# pprint.pprint(x.get_titles_grouped())

# # 10
# pprint.pprint(x.get_copy_data_with_new_id())

# 11
# pprint.pprint(x.get_collection_with_data())

# # 12
# pprint.pprint(x.write_data_in_csv())
