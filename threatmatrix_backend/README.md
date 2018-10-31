# ThreatMatrix - Backend

This project is intended to centralize information from a number of conflict-data 
related sources for analysis. The current main source of data is the [Armed Conflict 
Location & Event Data Project](https://www.acleddata.com/), with other planned for the
This project is currently a personal exercise and not for any commercial use, in line
with the ACLED terms of use (and other sources as they are added).

## Data Sources

[ACLED](https://www.acleddata.com/data/) - Beta

[World Bank](https://data.worldbank.org/) - Planned

## Structure

Each data sources is contained as a separate file, containing a `get_data`
method and any other helper functions required to get the data into a final,
usable DataFrame. These are called and processed through `main.py`, which handles
program flow and data insertion. General utilties, including databse insert operations
and common data cleaning may be extracted into `utilities.py`.

# Roadmap

In addition to data aggregation and cleaning, this module will hopefully 
eventually contain functionality for enhanced processing, including some
basic modeling and predictive analytics. These are solely for personal
practice and are not intended to provide useable data to policymakers or 
others interested in conflict studies, although they will most likely be
accompanied with a written analysis covering the methodology and appropriate
caveats.
