import argparse
import sys

from . import api
from . import models

class CLI:
    def __init__(self):
        """
        Start the command-line tool.
        """
        self.parse_arguments()
        self.search()

    def parse_arguments(self):
        """
        Parse supplied command line arguments.
        """
        self.parser = argparse.ArgumentParser(description="A command-line tool for retrieving an artist's filmography from IMDb.")
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--id", help="search by IMDb identifier")
        group.add_argument("--name", help="search by artist name")
        self.parser.add_argument("-r", "--reverse", action="store_true", help="display filmography in reverse order")
        self.parser.add_argument("-j", "--json", action="store_true", help="display filmography in machine-readable JSON")
        self.parser.add_argument("-o", "--output", metavar="FILE", help="save filmography to a file")
        self.arguments = self.parser.parse_args()

    def choose(self, options):
        """
        Display a choice between options.

        Returns early if only one option is provided.

        :param options: The options to choose between.
        :returns: The selected item.
        """
        if len(options) < 2:
            return options[0]

        print("Multiple results found:\n")

        for i, option in enumerate(options, 1):
            print(f"{i}:", option)

        print()

        while True:
            try:
                selection = options[int(input("> ")) - 1]
                print()
                return selection
            except (IndexError, ValueError):
                print("\nInvalid choice.\n")

    def display(self, actor):
        """
        Print an actor, in either plain-text or JSON based on configuration.

        :param actor: The actor to print.
        """
        if self.arguments.json:
            filmography = actor.json()
        else:
            filmography = actor.long()

        if self.arguments.output:
            with open(self.arguments.output, "w") as file:
                file.write(filmography)
        else:
            print(filmography)

    def get_actor(self):
        """
        Fetch an actor based on provided arguments.

        :returns: An Actor object.
        """
        if self.arguments.id:
            try:
                # A slightly risky way to fetch name, rank and known for
                actor = api.IMDb.actors(self.arguments.id)[0]

                # IMDb often doesn't return rank for ID-based searches
                if actor.rank == 0:
                    # search for actor by name
                    actors = api.IMDb.actors(actor.name)

                    for act in actors:
                        # find matching actor
                        if actor.identifier == act.identifier:
                            # return actor with rank instead
                            return act

                # rank present or lookup failed, returning original
                return actor
            except KeyError:
                pass

        elif self.arguments.name:
            actors = api.IMDb.actors(self.arguments.name)

            if actors:
                return self.choose(actors)

        else:
            # reached only for arguments like --name ""
            # argparse will throw before here for missing arguments
            print("No search target provided.")
            sys.exit(2) # command line error

        print("No results found from IMDB.")
        sys.exit(1) # unsuccessful

    def search(self):
        """
        Search for actors and filmographies based on provided arguments.
        """
        actor = self.get_actor()

        # fetch filmography
        actor.filmography = api.IMDb.actor(actor.identifier)

        # IMDb returns newest first by default
        if not self.arguments.reverse:
            actor.filmography.reverse()

        # display actor and filmography details
        self.display(actor)
