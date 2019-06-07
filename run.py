import sys

from core.application import Application

if __name__ == '__main__':
    app = Application()
    app.process_input(sys.argv[1:])
