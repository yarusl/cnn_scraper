import argparse
from constants import (SILENT_MODE, INTERACTIVE_MODE)


def parse_args():
    """
    Takes user input in CLI
    arg1: -u url of the section to scrape
    arg2: -p number of pages to scrape in the section
    """

    # Managing exceptions
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', type=str, help='foo help')
        parser.add_argument('-p', '--pages', type=int, default=1, help='baz help')
        args = vars(parser.parse_args())
    except ValueError as e:
        print(f"the user input in the CLI raised a ValueError: {e}. Beware of values")
    except TypeError as e:
        print(f"the user input in the CLI raised a TypeError: {e}. Please use the right type of input.")
    except SyntaxError as e:
        print(f"the user input in the CLI raised a SyntaxErrors: {e}. Please use the right type of input.")
    except Exception as e:
        print(f"the user input in the CLI raised an Exception: {e}. Please use the right type of input.")

    if args['url'] is None:
        mode = INTERACTIVE_MODE
    else:
        mode = SILENT_MODE
    return mode, args['url'], args['pages']
