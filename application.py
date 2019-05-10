#!/usr/bin/env python2

from flask import Flask, render_template
from database_setup import Category, Item, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

@app.route('/')
@app.route('/catalog/')
