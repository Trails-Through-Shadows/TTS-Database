import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

# Load the environment variables from .env file
load_dotenv('.env')

# ANSI color codes
colors = {
    "LIGHT_GRAY": '\033[37m',
    "GRAY":       '\033[90m',
    "INFO":       '\033[92m',
    "WARNING":    '\033[93m',
    "ERROR":      '\033[91m',
    "RESET":      '\033[0m',
}


# Log a message to the console
def log(message, level="INFO", reset=False):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    levelString = level.upper().ljust(6)
    print(f"{colors['GRAY']}[{current_time}] {colors[level]}{levelString}{colors['RESET']}: {message}", end='\r' if not reset else '\n')


# Retrieve database information from .env file
dbHost = os.getenv('DB_HOST')
dbUser = os.getenv('DB_USER')
dbName = os.getenv('DB_NAME')
dbPassword = os.getenv('DB_PASSWORD')

# Establish a database connection
try:
    log("Connecting to the database...", "INFO")
    conn = mysql.connector.connect(
        host=dbHost,
        user=dbUser,
        passwd=dbPassword,
        database=dbName
    )
    log("Connecting to the database... Done", "INFO", True)
except mysql.connector.Error as error:
    log(f"Error connecting to MySQL: {error}", "ERROR")
    exit(1)


# Function to execute a SQL file
def executeFileSQL(filePath: str) -> None:

    # Replace backslash with forward slash
    filePath = filePath.replace('\\', '/')

    with open(filePath, 'r') as file:
        sqlFileContent = file.read()
        cursor = conn.cursor()  # Create a new cursor for each file

        try:
            log(f"Executing {filePath}...", "INFO")

            # Execute the SQL file
            for result in cursor.execute(sqlFileContent, multi=True):
                pass  # Consuming the iterator

            conn.commit()
            log(f"Executing {filePath}... Done", "INFO", True)
        except mysql.connector.Error as error:
            conn.rollback()
            log(f"Executing {filePath}... Error: {error}", "ERROR", True)
        finally:
            cursor.close()
