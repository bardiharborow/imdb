import json
import re

class Actor:
    """
    An actor as stored in the IMDb database.
    """
    def __init__(self, identifier, name, rank, known_for, filmography):
        self.identifier = identifier
        self.name = name
        self.rank = rank
        self.known_for = known_for
        self.filmography = filmography

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.identifier == other.identifier and \
               self.name == other.name and \
               self.rank == other.rank and \
               self.known_for == other.known_for

    def __repr__(self):
        return f'{self.__class__.__name__}(identifier="{self.identifier}", name="{self.name}", rank={self.rank}, known_for="{self.known_for}", filmography={self.filmography})'

    def __str__(self):
        return f"{self.name}, ranked {self.rank}, known for {self.known_for}"

    def json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__, indent=4)

    def long(self):
        filmography = "\n".join(map(lambda s: str(s).replace("\n", ""), self.filmography))

        return (f"Name: {self.name}\n"
                f"Ranked: {self.rank}\n"
                f"Known for: {self.known_for}\n\n"
                f"Filmography ({len(self.filmography)} film{'' if len(self.filmography) == 1 else 's'}):\n\n{filmography}")

    @classmethod
    def from_imdb_suggestion(cls, suggestion):
        # strip IMDb's deduplication numerals
        # see <https://help.imdb.com/article/imdb/discover-watch/what-do-the-roman-numerals-like-i-and-ii-after-people-s-names-mean/GA827M8GK5KVH8TC>
        name = re.sub(" \\(.*\\)", "", suggestion["l"])

        return cls(suggestion["id"], name, suggestion["rank"] if "rank" in suggestion else 0, suggestion["s"], [])

class Role:
    """
    An actor's role in a movie as stored in the IMDb database.
    """
    def __init__(self, work, year, role):
        self.work = work
        self.year = year
        self.role = role

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.work == other.work and \
               self.year == other.year and \
               self.role == other.role

    def __repr__(self):
        return f'{self.__class__.__name__}(work="{self.work}", year="{self.year}", role="{self.role}")'

    def __str__(self):
        return f'{self.work} ({self.year or "???"}), as {self.role or "Unknown"}'
