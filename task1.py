import requests
from itertools import chain
from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta
import csv
import pprint
from consts import *


class Films:
    def __init__(self, pages):
        self.data = []
        self.get_data(pages)
        self.pairs = []
        self.collection = []

    # 1. Fetch the data from desired amount of pages
    def get_data(self, pages):
        results = [requests.get(url=URL.format(i), headers=HEADERS).json()['results'] for i in range(1, pages + 1)]
        self.data = list(chain.from_iterable(results))

        # # self comprehenision & flatten (chain.from_sequence)
        # for i in range(1, pages + 1):
        #     response = requests.get(url=URL.format(i), headers=HEADERS)
        #     self.data.extend(response.json()['results'])

    # 2. Give a user all data
    def get_all_data(self):
        return self.data

    # 3. All data about movies with indexes from 3 till 19 with step 4
    def slicing_data(self):
        return self.data[3:19:2]

    # 4. Name of the most popular title
    def get_most_popular_title(self):
        return max(self.data, key=lambda a: a[POPULARITY])[TITLE]

    # 5. Names of titles which has in description keywords which a user put as parameters
    def get_title_by_key_words(self, keywords):
        return [film[TITLE] for film in self.data if any(keyword in film[OVERVIEW] for keyword in keywords)]

    # 6. Unique collection of present genres (the collection should not allow inserts)
    def get_unique_genres(self):
        return frozenset(genre for film in self.data for genre in film.get(GENRE_IDS, []))

    # 7. Delete all movies with user provided genre
    def delete_movies(self, num_genre):
        return list(filter(lambda film: num_genre not in film[GENRE_IDS], self.data))

    # 8. Names of most popular genres with numbers of time appear in the data
    def get_most_popular_genres(self):
        return dict(Counter(genre for film in self.data for genre in film[GENRE_IDS]).most_common())

    # 9. Collection of film titles  grouped in pairs by common genres (the groups should not allow inserts)
    def get_titles_grouped(self):
        return [(first_film[TITLE], second_film[TITLE]) for first_film in self.data for second_film in \
                self.data if first_film[TITLE] != second_film[TITLE] and \
                set(first_film[GENRE_IDS]).intersection(second_film[GENRE_IDS])]

    # 10. Return initial data and copy of initial data where first id in list of film genres was replaced with 22
    def get_copy_data_with_new_id(self):
        copy_data = deepcopy(self.data)
        for i in copy_data:
            i[GENRE_IDS][0] = 22
        return self.data, copy_data

    # 11. Collection of structures with part of initial data which has the following fields:
    #   •	Title
    #   •	Popularity (with 1 decimal point with maximum precision)
    #   •	Score (vote_average without fractional part)
    #   •	Last_day_in_cinema (2 months and 2 weeks after the release_date)
    #   Collection should be sorted by score and popularity
    def get_collection_with_data(self):
        self.collection = [
            {
                'Title': film[TITLE],
                'Popularity': round(film[POPULARITY], 1),
                'Score': int(film[VOTE_AVERAGE]),
                'Last day in cinema': (datetime.strptime(film[RELEASE_DATE], DATA_FORMAT) +
                                       timedelta(weeks=8, days=4)).strftime(DATA_FORMAT)
            }
            for film in self.data
        ]
        self.collection.sort(key=lambda f: (f[SCORE], f['Popularity']))
        return self.collection

    # 12. Write information from previous step to a csv file using path provided by user
    def write_data_in_csv(self):
        with open(FILE_WITH_FILMS, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, FIELDS)
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
# keywords = input("Find: ").split()
# pprint.pprint(x.get_title_by_key_words(keywords))

# # 6
# pprint.pprint(x.get_unique_genres())

# # 7
# num_genre = input('Delete (number of genre): ')
# pprint.pprint(x.delete_movies(num_genre))

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
