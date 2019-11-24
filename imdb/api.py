import html.parser
import json
import requests

from . import models

class IMDbFilmographyParser(html.parser.HTMLParser):
    """
    This class scrapes IMDb actor pages for their filmography. IMDb's HTML is
    extermely non-compliant, so this is anticipated to be fragile. We use a
    state machine to keep track of where we are and try not to get tangled.
    """
    def __init__(self):
        """
        Initialize the filmography parser.
        """
        super().__init__()

        # 0 - outside film, 1 - inside film, 2 - year, 3 - title, 4 - role
        self.state = 0

        # parsed filmography
        self.filmography = []

        # current film details
        self.year = ""
        self.work = ""
        self.role = ""

    def handle_starttag(self, tag, attrs):
        # inside film -> title
        if self.state == 1 and tag == "b":
            self.state = 3

        # role -> inside film
        elif self.state == 4 and tag == "div":
            self.state = 1

        elif self.state in (0, 1):
            attributes = dict(attrs)

            if "class" in attributes:
                classes = attributes["class"].split()
                actor_role = "id" in attributes and attributes["id"].startswith("act")

                # outside film -> inside film
                if self.state == 0 and "filmo-row" in classes and actor_role:
                    self.state = 1

                # inside film -> year
                elif self.state == 1 and "year_column" in classes:
                    self.state = 2

    def handle_endtag(self, tag):
        # inside film or role -> outside film
        if self.state in (1, 4) and tag == "div":
            role = models.Role(self.work.strip(),
                               self.year.strip(),
                               self.role.strip())

            self.filmography.append(role)

            self.state = 0
            self.year = ""
            self.work = ""
            self.role = ""

        # inside film -> role
        elif self.state == 1 and tag == "br":
            self.state = 4

        # year -> inside film
        elif self.state == 2 and tag == "span":
            self.state = 1

        # title -> inside film
        elif self.state == 3 and tag == "b":
            self.state = 1

    def handle_data(self, data):
        # collect year
        if self.state == 2:
            self.year += data

        # collect title
        elif self.state == 3:
            self.work += data

        # collect role
        elif self.state == 4:
            self.role += data

class IMDb:
    """
    An interface to the IMDb Suggestions API and scraping of Actor pages.
    """
    suggestions_endpoint = "https://v2.sg.media-imdb.com/suggestion/"
    actor_endpoint = "https://www.imdb.com/name/"

    @staticmethod
    def actors(name):
        """
        Search for actors by name.

        :param name: The name.
        :returns: A list of potential Actor objects.
        """
        safe_name = name.lower().replace(" ", "_")

        url = f"{IMDb.suggestions_endpoint}names/{safe_name[0]}/{safe_name}.json"

        response = requests.get(url)

        if response:
            payload = json.loads(response.text)

            try:
                return list(map(models.Actor.from_imdb_suggestion, payload["d"]))
            except:
                raise RuntimeError("Parsing IMDB results failed.")

        raise RuntimeError("Fetching IMDB results failed.")

    @staticmethod
    def actor(identifier):
        """
        Lookup an actor's filmography by IMDb identifier.

        :param identifier: The actor's IMDb identifier.
        :returns: A list of Role objects.
        """
        url = f"{IMDb.actor_endpoint}{identifier}/"

        response = requests.get(url)

        parser = IMDbFilmographyParser()
        parser.feed(response.text)

        return parser.filmography
