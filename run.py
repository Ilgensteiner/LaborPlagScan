import sys

from laborPlagScan import main
import laborPlagScan.basicConfig as basicConfig


if __name__ == '__main__':
    sys.excepthook = basicConfig.handle_exception
    main.run()
