from urllib.parse import urljoin

import requests



class GhibliApi:
    """Main interface to interact with the Ghibli Studio API."""

    _base_url = 'https://ghibliapi.vercel.app'

    _films_url = _base_url + '/films'
    _people_url = _base_url + '/people'
    

    @classmethod
    def get_film_list_with_cast(cls) :
        """Returns a list of all films from Ghibli Studio API including
        people that appear in it.

        e.g.
        id: film id in Ghibli Studio API
        title: film's title
        people: list of person's name that appear in the films.

        [{'id':'45336', 'title':'Totoro', 'people':['Renaldo',]}]
        """

        films_with_people = cls.query_films().copy()

        # for every person get all film's id
        for person in cls.query_people():
            for person_film_id in person['films_id']:

                # and compare film id with person's film id
                for film in films_with_people:
                    if person_film_id == film['id']:

                        # people key don't exist. create it.
                        if not isinstance(film.get('people'), list):
                            film['people'] = []

                        film['people'].append(person['name'])

        return films_with_people

    @classmethod
    def query_films(cls) :
        """Requests all films available from Ghibli
        and return a list with title and film id.
        """

        films_data = requests.get(cls._films_url).json()
        films = [cls.parse_film_title_and_id(film) for film in films_data]

        return films

    @classmethod
    def query_people(cls):
        """Requests all people that appear in Ghibli films and
        returns a list with people's name and a list of films id.
        """

        people_data = requests.get(cls._people_url).json()
        people = [
            cls.parse_name_and_films_id(person)
            for person in people_data
        ]

        return people

    @classmethod
    def parse_film_title_and_id(cls, film) :
        """Extracts from the film data the title and id."""

        return {
            'id': film.get('id'),
            'title': film.get('title'),
            'species' : film.get('species'),
            'url' : film.get('url'),
            'actors' : film.get('people')
        }

    @classmethod
    def parse_name_and_films_id(cls, person) :
        """Extracts from the person data.their name and films id."""

        return {
            'name': person.get('name'),
            'films_id': [
                cls.parse_film_id_from_url(film)
                for film in person.get('films')
            ],
        }

    @classmethod
    def parse_film_id_from_url(cls, film: str) -> str:
        """Extracts the film id from full URL."""

        return film.split('/')[-1]



print(GhibliApi.query_films())