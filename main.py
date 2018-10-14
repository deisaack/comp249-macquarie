__author__ = ''

import random

from bottle import Bottle, template, static_file

from interface import position_get
import interface

app = Bottle()


COLOR_CHOICES = (
    "#703907", '#677007', "#08704a", "#0ccc85", '#0ca2cc', '#0c58cc', "#cc0c19", '#660d30', '#610d66',
    "#300d66", "#FFB593", "#0d2f66"
)

@app.route('/')
@app.route('/positions/')
@app.route('/positions/page=<page>')
def index(db, page=1):
    PAGE_SIZE = 12              # Number of positions to display per page
    end = int(page) * PAGE_SIZE      # The last positions
    start = end - PAGE_SIZE     #

    list = interface.position_list(db, limit=1)


    i = 0
    position_list = list[start:end]
    positions = []
    for position in position_list:
        # Convert the tuple to a dictionary and Add a random color for displaying the position
        obj = {
            "id": position[0],
            "color": COLOR_CHOICES[random.randint(0, len(COLOR_CHOICES)-1)],
            "timestamp": position[1],
            "owner": position[2],
            "title": position[3],
            "location": position[4],
            "company": position[5],
            "description": position[6]
        }
        positions.append(obj)




    info = {
        'title': 'My Website',
        'positions': positions,
        'next': "/positions/page=" + str(int(page)+1),
        'previous': "/positions/page=" + str(int(page) - 1)
    }

    return template('index', info)



@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


@app.route('/about/')
@app.route('/about')
def about():
    obj = {
        "title": "About Us"
    }
    return template('about', obj)


@app.route('/positions/<id>/')
def position_detail(db, id):
    """
    Retrieves a position with the given id
    :param db: Database comnnection
    :param id: ID of the position
    :return: The page with content
    """
    position = position_get(db, id)
    obj = {
        "id": position[0],
        "color": COLOR_CHOICES[random.randint(0, len(COLOR_CHOICES) - 1)],
        "timestamp": position[1],
        "owner": position[2],
        "title": position[3],
        "location": position[4],
        "company": position[5],
        "description": position[6],
        'next': "/position/" + str(int(id) + 1) + "/",
        'previous': "/position/" + str(int(id) - 1) + "/"
    }
    return template('position_detail', obj)





if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8000)
