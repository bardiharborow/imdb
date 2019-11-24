import argparse

from . import api

class CLI:
    def __init__(self):
        """
        Start the command-line tool.
        """
        self.parse_arguments()
        self.run()

    def parse_arguments(self):
        """
        Parse supplied command line arguments.
        """
        self.parser = argparse.ArgumentParser(description="A command-line tool for retrieving an artist's filmography from IMDb.")
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--id", help="search by IMDb identifier")
        group.add_argument("--name", help="search by artist name")
        self.parser.add_argument("--reverse", action="store_true", help="display filmography in reverse order")
        self.parser.add_argument("--json", action="store_true", help="display filmography in machine-readable JSON")
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
            print(actor.json())
        else:
            print(actor.long())

    def run(self):
        """
        Search for actors and filmographies based on provided arguments.
        """
        if self.arguments.id:
            raise NotImplementedError
        elif self.arguments.name:
            actors = api.IMDb.actors(self.arguments.name)
        else:
            # never reached as argparse will throw first
            raise RuntimeError("No search target provided.")

        if actors:
            selection = self.choose(actors)

            selection.filmography = api.IMDb.actor(selection.identifier)

            if self.arguments.reverse:
                selection.filmography.reverse()

            self.display(selection)
        else:
            print("No results found from IMDB.")
