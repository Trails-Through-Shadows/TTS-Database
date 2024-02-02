# TTS-Database

This repo contains scripts for managing (creating, dropping and filling) the main TTS testing database.

## Setup
- Make sure you have your virtual environment set up properly
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Make sure all requirements are installed
  - `pip install -r requirements.txt`
- Create .env file
  - `cp .env.example .env`
  - update .env file with your credentials
 
## Run
The database is equipped with the following scripts, located in the `script` folder:
- `create.py`: creates the database and fills it with testing data
  - `-s` flag skips the insert phase
- `drop.py`: drops the entire database
- `insert.py`: clears and re-inserts testing data into the database
  - `-s` flag skips the clear phase

Run these scripts with a command such as `python3 script/create.py`.

## Schema

The database diagram can be found [here](https://dbdiagram.io/d/CommunistBachelor-652c00e7ffbf5169f0b71ee4), if you have access of course.

When the diagram is updated, just export it into MySql and copy the contens into `manage/create.sql` and update the inserting scripts to go with your changes.
