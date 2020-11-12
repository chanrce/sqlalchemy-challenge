import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Import Flask
from flask import Flask, jsonify



#Create an app

app = Flask(__name__)

#Define static routes