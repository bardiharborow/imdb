# Sample data is Copyright (c) 1990-2019 IMDb.com, Inc.

import unittest

from imdb.models import Actor, Role

class TestActor(unittest.TestCase):
    def setUp(self):
        self.actor = Actor("nm0850102", "Amanda Tapping", 2441,
                           "Actress, Stargate SG-1 (1997-2007)", [Role("Sanctuary", "2008-2011", "Dr. Helen Magnus")])
        self.actor2 = Actor("nm0850102", "Amanda Tapping", 2441,
                           "Actress, Stargate SG-1 (1997-2007)", [Role("Sanctuary", "2008-2011", "Dr. Helen Magnus")])
        self.actor3 = Actor("nm0850102", "Amanda Tapping", 2441,
                           "Actress, Stargate SG-1 (1997-2007)", [])

    def test___eq__(self):
        self.assertEqual(self.actor, self.actor2)

    def test___repr__(self):
        self.assertEqual(repr(self.actor), 'Actor(identifier="nm0850102", name="Amanda Tapping", rank=2441, known_for="Actress, Stargate SG-1 (1997-2007)", filmography=[Role(work="Sanctuary", year="2008-2011", role="Dr. Helen Magnus")])')

    def test___str__(self):
        self.assertEqual(str(self.actor), "Amanda Tapping, ranked 2441, known for Actress, Stargate SG-1 (1997-2007)")

    def test_json(self):
        self.assertEqual(self.actor.json(), """{
    "identifier": "nm0850102",
    "name": "Amanda Tapping",
    "rank": 2441,
    "known_for": "Actress, Stargate SG-1 (1997-2007)",
    "filmography": [
        {
            "work": "Sanctuary",
            "year": "2008-2011",
            "role": "Dr. Helen Magnus"
        }
    ]
}""")
        self.assertEqual(self.actor3.json(), """{
    "identifier": "nm0850102",
    "name": "Amanda Tapping",
    "rank": 2441,
    "known_for": "Actress, Stargate SG-1 (1997-2007)",
    "filmography": []
}""")

    def test_long(self):
        self.assertEqual(self.actor.long(), "Name: Amanda Tapping\nRanked: 2441\nKnown for: Actress, Stargate SG-1 (1997-2007)\n\nFilmography (1 film):\n\nSanctuary (2008-2011), as Dr. Helen Magnus")
        self.assertEqual(self.actor3.long(), "Name: Amanda Tapping\nRanked: 2441\nKnown for: Actress, Stargate SG-1 (1997-2007)\n\nFilmography (0 films):\n\n")

    def test_from_imdb_suggestion(self):
        payload = {
            "id": "nm0850102",
            "l": "Amanda Tapping",
            "rank": 2441,
            "s": "Actress, Stargate SG-1 (1997-2007)"
        }

        actor = Actor.from_imdb_suggestion(payload)

        self.assertEqual(actor, Actor("nm0850102", "Amanda Tapping", 2441, "Actress, Stargate SG-1 (1997-2007)", []))

class TestRole(unittest.TestCase):
    def setUp(self):
        self.role = Role("Madam C.J. Walker", "2020", "Sarah Breedlove")
        self.role2 = Role("Madam C.J. Walker", "2020", "Sarah Breedlove")
        self.role3 = Role("", "", "")

    def test___eq__(self):
        self.assertEqual(self.role, self.role2)

    def test___repr__(self):
        self.assertEqual(repr(self.role), 'Role(work="Madam C.J. Walker", year="2020", role="Sarah Breedlove")')

    def test___str__(self):
        self.assertEqual(str(self.role), "Madam C.J. Walker (2020), as Sarah Breedlove")
        self.assertEqual(str(self.role3), " (???), as Unknown")

if __name__ == "__main__":
    unittest.main()
