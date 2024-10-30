#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/opt/flask_form")
 
from app import app as application
application.secret_key = "fhkjdskjgf(anything)"