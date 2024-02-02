# TTS-Database

This repo contains scripts for managing (creating, dropping and filling) the main TTS testing database.

## Setup
- Make sure you have your virtual environment set up properly
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Make sure all requirements are met
  - `pip install -r requirements.txt`
- Create .env file
  - `cp .env.example .env`
  - update .env file with your credentials
 
## Run
The database is equipped with the following scripts, located in the `script` folder:
- **Create**: creates the database and fills it with testing data
- **Drop**: drops the entire database
- **Insert**: inserts testing data into the database

Run these scripts with `python3 script/create.py`.

## Schema

The database diagram can be found [here](https://dbdiagram.io/d/CommunistBachelor-652c00e7ffbf5169f0b71ee4), if you have access of course.

When the diagram is updated, just export it into MySql and copy the contens into `manage/create.sql` and update the inserting scripts to go with your changes.
