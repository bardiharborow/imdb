# Sample data is Copyright (c) 1990-2019 IMDb.com, Inc.

import requests
import unittest

from unittest.mock import Mock, patch

from imdb.api import IMDb, IMDbFilmographyParser
from imdb.models import Actor, Role

class TestIMDbFilmographyParser(unittest.TestCase):
    def setUp(self):
        self.parser = IMDbFilmographyParser()
        self.simple_sample = """
            <div class="filmo-row odd" id="actor-tt0119116">
            <span class="year_column">
            &nbsp;1997
            </span>
            <b><a href="/title/tt0119116/?ref_=nm_flmg_act_89"
            >The Fifth Element</a></b>
            <br/>
            Korben Dallas
            </div>
        """

        self.complex_sample = """
            <div class="filmo-row odd" id="actress-tt8771910">
            <span class="year_column">
            &nbsp;2020
            </span>
            <b><a href="/title/tt8771910/?ref_=nm_flmg_act_3"
            >Madam C.J. Walker</a></b>
            (TV Series) (<a href="https://pro.imdb.com/title/tt8771910?rf=cons_nm_filmo&ref_=cons_nm_filmo"
            class="in_production">filming</a>)
            <br/>
            Sarah Breedlove
            <div class="filmo-episodes">
            - <a href="/title/tt8772006/?ref_=nm_flmg_act_3"
            >Episode #1.1</a>
            (2020)
            ... Sarah Breedlove
            </div>
            <div class="filmo-episodes">
            - <a href="/title/tt8782526/?ref_=nm_flmg_act_3"
            >Episode #1.8</a>
            ... Sarah Breedlove
            </div>
            <div class="filmo-episodes">
            - <a href="/title/tt8782512/?ref_=nm_flmg_act_3"
            >Episode #1.7</a>
            ... Sarah Breedlove
            </div>
            <div class="filmo-episodes">
            - <a href="/title/tt8782506/?ref_=nm_flmg_act_3"
            >Episode #1.6</a>
            ... Sarah Breedlove
            </div>
            <div class="filmo-episodes">
            - <a href="/title/tt8782498/?ref_=nm_flmg_act_3"
            >Episode #1.5</a>
            ... Sarah Breedlove
            </div>
            <div id="more-episodes-tt8771910-actress" style="display:none;">
            <img src="https://m.media-amazon.com/..." />
            </div>
            <div class="filmo-episodes">
            <a href="#"
            data-n="8"
            onclick="...">Show all 8 episodes</a>
            </div>
            </div>
        """

    def test_simple(self):
        self.parser.feed(self.simple_sample)
        self.assertEqual(self.parser.filmography[0], Role("The Fifth Element", "1997", "Korben Dallas"))

    def test_complex(self):
        self.parser.feed(self.complex_sample)
        self.assertEqual(self.parser.filmography[0], Role("Madam C.J. Walker", "2020", "Sarah Breedlove"))

class TestIMDb(unittest.TestCase):
    def setUp(self):
        TestIMDbFilmographyParser.setUp(self)
        self.suggestions_sample = """
            {
              "d": [
                {
                  "i": {
                    "height": 1280,
                    "imageUrl": "https://m.media-amazon.com/...",
                    "width": 1038
                  },
                  "id": "nm0914612",
                  "l": "Emma Watson (II)",
                  "rank": 201,
                  "s": "Actress, The Perks of Being a Wallflower (2012)",
                  "v": [],
                  "vt": 87
                }
              ],
              "q": "emma watson",
              "v": 1
            }
        """

    def test_actors(self):
        response = Mock()
        response.text = self.suggestions_sample
        requests.get = Mock(return_value=response)

        actors = IMDb.actors("Emma Watson")

        self.assertEqual(actors[0], Actor("nm0914612", "Emma Watson", 201, "Actress, The Perks of Being a Wallflower (2012)", []))
        requests.get.assert_called_with("https://v2.sg.media-imdb.com/suggestion/names/e/emma_watson.json")

    def test_actor(self):
        response = Mock()
        response.text = self.complex_sample
        requests.get = Mock(return_value=response)

        filmography = IMDb.actor("nm0818055")

        self.assertEqual(filmography[0], Role("Madam C.J. Walker", "2020", "Sarah Breedlove"))
        requests.get.assert_called_with("https://www.imdb.com/name/nm0818055/")

if __name__ == "__main__":
    unittest.main()
