# Panorma-bot

This scraper for climate indicator data from <a href="https://app.climateview.global/sweden">Panorama</a>. It gathers scenario and obesvation data in csv file for analysis.

The scraper is limited to transition indicators. It does not handle policies ("Styrmedel och åtaganden").

The scraper has not formal relationship with Panorama. 

## Install

    pip install -r requirements.txt

## Scripts


- `scrape.py`: Downloads a snapshot with data for all indicators.
- `evaluated_downloaded.py`: Checks if a downloaded file differs from the previously downloaded data.
- `parse_raw.py`: Parses time series data from downloaded data.

## Data

`data/parsed/latest` contains the latest version of the indicator data.

`data/parsed/[timestamp]` represents older snapshots.

## Actions

The scraper is scheduled to run daily with Github Actions.