import csv 
import sqlalchemy
import folium
import pandas as pd
import cgi
import re

from pathlib import Path
from bokeh.models.widgets import RangeSlider, Button, DataTable, \
    TableColumn, NumberFormatter 
from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure, show
from bokeh.layouts import row, widgetbox
from branca.colormap import LinearColormap
from threatmatrix.db import db_location


def get_data(n): 
    engine = sqlalchemy.create_engine(db_location)
    conn = engine.connect()

    df = pd.read_sql('events', conn)[:n]
    df['notes'] = df['notes'].map(clean_note)
    return df 


def clean_note(note):
    note = note.replace("'", "").replace('"', '')

    if len(note) > 100:
        parts = []
        for i in range(0, len(note.split()), 10):
            parts.append(' '.join(note.split()[i:i+10]))
        note = '<br>'.join(parts)
    return note


def create_map(df, map_type):
    if map_type == 'choropleth':
        create_choropleth(df, columns=['country', 'fatalities'])
    elif map_type == 'points':
        create_points(df)


def create_points(df):
    m = folium.Map(location=[35, 55], zoom_start=5)

    points = df[['latitude', 'longitude', 'notes']].values.tolist() 

    for i in range(len(points)):
        folium.Marker([float(points[i][0]), float(points[i][1])], 
            tooltip=points[i][2]).add_to(m)

    m.save(Path(__file__).parent + '/maps/points.html')


def get_color(feature, map_dict, columns, color_scale):
    value = map_dict.get(feature['properties']["ADMIN"])
    if value is None:
        return '#8c8c8c' # MISSING -> gray
    else:
        return color_scale(value)


def create_choropleth(df, columns):
    df[columns[1]] = pd.to_numeric(df[columns[1]], downcast='integer').fillna(0)
    df = df.groupby(columns[0]).sum()[columns[1]].to_frame().reset_index()
    map_dict = df.set_index(columns[0])[columns[1]].to_dict()

    country_geo = Path(__file__).parent + '/assets/countries.geojson'
    color_scale = LinearColormap(['yellow','red'], vmin=min(map_dict.values()),
                                 vmax=max(map_dict.values()))

    m = folium.Map(location=[0, 0], zoom_start=3, width='80%')

    folium.GeoJson(
        data = country_geo,
        style_function = lambda feature: {
            'fillColor': get_color(feature, map_dict, columns, color_scale),
            'fillOpacity': 0.7,
            'color' : 'black',
            'weight' : 1,
        }    
    ).add_to(m)

    m.save(Path(__file__).parent + '/maps/choropleth.html')


def create_bar_chart(df):
    df['fatalities'] = pd.to_numeric(df['fatalities'])
    df['fatalities'] = df['fatalities'].fillna(0)

    sums = df.groupby('iso3')['fatalities'].sum().sort_values()
    sums = sums[sums > 0]
    countries = sums.index.values
    counts = sums.values

    p = figure(x_range=countries, plot_height=250, 
               title="Fatalities by Country")
    p.vbar(x=countries, top=counts, width=0.5)
    p.y_range.start = 0
    p.xgrid.grid_line_color = None

    return p

def create_table(df):
    source = ColumnDataSource(data=dict())
    current = df.sort_values('fatalities', ascending=False).head(10)

    source.data = {
        'Country'             : current.country,
        'Date'                : current.event_date,
        'Fatalities'          : current.fatalities,
        'Description'         : current.notes,
    }

    columns = [
        TableColumn(field="Country", title="Country"),
        TableColumn(field="Date", title="Date"),
        TableColumn(field="Fatalities", title="Fatalities"),
        TableColumn(field="Description", title="Description")
    ]

    data_table = DataTable(source=source, columns=columns, width=800)

    table = widgetbox(data_table)

    return table
