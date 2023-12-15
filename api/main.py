""" We're not sure if this actually needed or not. Probably not? """
import os
import sys

# forced import hints for pyinstaller (for one day making this an application)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
