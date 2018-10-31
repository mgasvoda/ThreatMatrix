# ThreatMatrix - Frontend

This project is intended to centralize information from a number of conflict-data 
related sources for analysis. Currently, the framework supports mapping of points and 
genral country-level polygons through Folium, and general interactive plots and tables
through Bokeh. In addition to generic interactive data exploration, written analysis
can be supported using flasks's jinja templating support. Where possible, all data 
processing, cleaning, and transormations are handled in the threatmatrix_backend 
package to minimize performance issues, although there are ceratinly a number of 
performance areas that already need improvement. 

## Data Sources

[ACLED](https://www.acleddata.com/data/) - Beta

[World Bank](https://data.worldbank.org/) - Planned

## Usage

After the repository has been cloned and connected to the appropriate database,
`flask run` will start the project, on http://localhost:5000 by default. Maps 
and charts are generated on page load, so you will likely experience slow loading times
on pages including visualization - this will be addressed in the future. 
