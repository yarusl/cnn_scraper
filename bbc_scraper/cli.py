import argparse
from constants import (SILENT_MODE, INTERACTIVE_MODE)

def parse_args():    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='foo help')
    parser.add_argument('-p', '--pages', type=int, default=1, help='baz help')
    args = vars(parser.parse_args())
    
    mode = SILENT_MODE
    if args['url'] is None:
        mode = INTERACTIVE_MODE    
    return mode, args['url'], args['pages']
