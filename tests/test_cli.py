import unittest
import sys
import builtins

from unittest.mock import Mock, patch

from imdb.cli import CLI
from imdb.models import Actor, Role

class TestCLI(unittest.TestCase):
    def test_parse_arguments(self):
        args = ["imdb", "--id", "nm0000608"]
        with unittest.mock.patch.object(sys, 'argv', args):
            CLI.parse_arguments(self)

        self.assertEqual(self.arguments.id, "nm0000608")
        self.assertEqual(self.arguments.name, None)
        self.assertEqual(self.arguments.reverse, False)
        self.assertEqual(self.arguments.json, False)
        self.assertEqual(self.arguments.output, None)

        for args in (["imdb", "--name", "Burt Reynolds", "--reverse", "--json", "--output", "demo.json"],
                     ["imdb", "--name", "Burt Reynolds", "-r", "-j", "-o", "demo.json"]):
            with unittest.mock.patch.object(sys, 'argv', args):
                CLI.parse_arguments(self)

            self.assertEqual(self.arguments.id, None)
            self.assertEqual(self.arguments.name, "Burt Reynolds")
            self.assertEqual(self.arguments.reverse, True)
            self.assertEqual(self.arguments.json, True)
            self.assertEqual(self.arguments.output, "demo.json")

    @patch("builtins.print")
    def test_display(self, print):
        self.arguments = Mock()

        self.arguments.json = False
        self.arguments.output = None

        CLI.display(self, Actor("nm0850102", "Amanda Tapping", 2441,
                          "Actress, Stargate SG-1 (1997-2007)",
                          [Role("Sanctuary", "2008-2011", "Dr. Helen Magnus")]))

        print.assert_called_once_with("Name: Amanda Tapping\nRanked: 2441\nKnown for: Actress, Stargate SG-1 (1997-2007)\n\nFilmography (1 film):\n\nSanctuary (2008-2011), as Dr. Helen Magnus")

        print.reset_mock()
        self.arguments.json = True

        CLI.display(self, Actor("nm0850102", "Amanda Tapping", 2441,
                          "Actress, Stargate SG-1 (1997-2007)",
                          [Role("Sanctuary", "2008-2011", "Dr. Helen Magnus")]))

        print.assert_called_once_with("""{
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

if __name__ == "__main__":
    unittest.main()
