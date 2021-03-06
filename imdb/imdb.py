import requests
from bs4 import BeautifulSoup
from movies.movies import Movie


class IMDB:
    __url__ = 'http://www.imdb.com'
    movies = {"new": "movies-coming-soon/{0}/?ref_=inth_cs", "intheaters": "movies-in-theaters/?ref_=cs_inth"}

    @staticmethod
    def getmovies(desc, date):
        films = []
        if desc in IMDB.movies:
            page = requests.get('/'.join((IMDB.__url__, IMDB.movies[desc])).format(date))
            soup = BeautifulSoup(page.content, "html.parser")
            items = soup.find_all('div', class_="list_item")
            for movie in items:
                title = movie.find('h4').get_text()
                duration = movie.find('time').get_text() if movie.find('time') else '0'
                summary = movie.find('div', class_='outline').get_text() if movie.find('div',
                                                                                       class_='outline').get_text() else ''
                genre = [genre.get_text() for genre in movie.find_all('span', {'itemprop': 'genre'})]
                cast = [actor.get_text() for actor in movie.find_all('span', {'itemprop': 'actors'})]
                directors = [director.get_text() for director in movie.find_all('span', {'itemprop': 'director'})]
                trailers = [trailer.attrs['href'] for trailer in movie.find_all('a', {'itemprop': 'trailer'})]
                film = Movie(title, directors, duration, genre, summary, cast, trailers)
                films.append(film)
        return films
