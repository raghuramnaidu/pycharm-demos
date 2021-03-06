import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template
from psycopg2.extras import NamedTupleCursor

load_dotenv()
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

conn = psycopg2.connect(os.environ['POSTGRES_DSN'])

actors_query = 'SELECT actor_id, first_name, last_name FROM actor LIMIT 20'


# ----- Home page
@app.route('/')
def homepage_index():
    title = f'Sakila Homepage'
    return render_template('homepage.jinja2', title=title)


@app.route('/actors/')
def actors_index():
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(actors_query)
        actors = cur.fetchall()
        cur.close()

        title = f'Actors'
        return render_template('actors.jinja2', title=title, actors=actors)


@app.route('/actors/<int:actor_id>')
def actor_index(actor_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(actors_query)
        actors = cur.fetchall()

        actor_query = 'SELECT * from actor WHERE actor_id = %s'
        cur.execute(actor_query, (actor_id,))
        actor = cur.fetchone()

        cur.close()

        title = f'Actor: {actor.first_name} {actor.last_name}'
        return render_template('actor.jinja2', actors=actors, actor=actor, title=title)
