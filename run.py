from UIs.terminal_UI import *
from UIs.web_UI import *
import argparse


def run ():
    parser = argparse.ArgumentParser()
    parser.add_argument("--terminal", action="store_true", help="Run using Terminal UI")
    args = parser.parse_args()
    # if (args.terminal == True):
    Terminal()
    # else:
    #     webUI()
        
if __name__ == '__main__':
    run()