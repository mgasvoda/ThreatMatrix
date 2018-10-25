import sqlalchemy
import folium
import processing
import markdown
import os

from bokeh.embed import components
from flask import Flask, redirect, url_for, render_template, send_file, Markup

app = Flask(__name__)

df = processing.get_data(250)

@app.route("/")
def hello():
    # with open(os.path.join(__file__ "README.md", 'r') as f:
    path = os.path.abspath('README.md')
    with open(path, 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('index.html', **locals())


@app.route("/maps.html")
def display():
    return render_template('maps.html')


@app.route("/plots.html")
def show_plots():
  plot = processing.create_bar_chart(df)
  plot_script, plot_div = components(plot)
  table = processing.create_table(df)
  table_script, table_div = components(table)
  return render_template("charts.html", plot_div=plot_div, plot_script=plot_script,
                         table_div=table_div, table_script=table_script)


@app.route('/maps/points.html')
def show_map_points():
  processing.create_map(df, 'points')
  return send_file('./maps/points.html')


@app.route('/maps/choropleth.html')
def show_map_choro():
  processing.create_map(df, 'choropleth')
  return send_file('./maps/choropleth.html')


@app.route('/blog')
def show_blog():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'posts\\sample.md')    
    with open(path, 'r') as f:
        content = f.read()
    content = Markup(markdown.markdown(content))
    return render_template('blog.html', **locals())
