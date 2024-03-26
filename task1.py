import requests

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNT"
                     "UyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMD"
                     "FmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW"
                     "9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
}


class Films:
    def __init__(self, pages):
        self.data = []
        self.get_data(pages)

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


x = Films(3)


# # 2
# print(x.get_all_data())

# # 3
# print(x.slicing_data())

# # 4
# print(x.get_most_popular_title())

# # 5
# print(x.get_title_by_key_words())

# # 6
# print(x.get_unique_genres())

# 7


# 8
