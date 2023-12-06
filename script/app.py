import os
import mysql.connector
import subprocess
from dotenv import load_dotenv
from datetime import datetime

# Load the environment variables from .env file
load_dotenv('.env')

# ANSI color codes
colors = {
    "LIGHT_GRAY": '\033[37m',
    "GRAY":       '\033[90m',
    "INFO":       '\033[92m',
    "DEBUG":      '\033[94m',
    "WARNING":    '\033[93m',
    "ERROR":      '\033[91m',
    "RESET":      '\033[0m',
}


# Log a message to the console
def log(message, level="INFO", reset=False):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    levelString = level.upper().ljust(6)

    # Replace the level with the colorized level
    message = message.replace("Error", f"{colors['ERROR']}Error{colors['RESET']}")
    message = message.replace("Done", f"{colors['INFO']}Done{colors['RESET']}")

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
    log("Connecting to the database... Error", "INFO", True)
    log(f" - {error}", "ERROR")
    exit(1)


# Function to execute a SQL file
def executeFileSQL(filePath: str) -> None:
    filePath = filePath.replace('\\', '/')
    log(" - Executing {}...".format(filePath), "INFO")

    try:
        # Read the SQL file
        file = open(filePath, "r")
        sqlFileContent = file.read()
        file.close()

        # Execute the SQL file
        cursor = conn.cursor()
        for result in cursor.execute(sqlFileContent, multi=True):
            pass  # Consuming the iterator

        conn.commit()
        log(" - Executing {}... Done".format(filePath), "INFO", True)
    except Exception as e:
        log(" - Executing {}... Error".format(filePath, e), "INFO", True)
        log("    - {}".format(e), "ERROR", True)


# Function to execute a Python file
def executeFilePython(filePath: str) -> None:
    filePath = filePath.replace('\\', '/')
    log(" - Executing {}...".format(filePath), "INFO")

    try:
        subprocess.call(['python', filePath])
        log(" - Executing {}... Done".format(filePath), "INFO", True)
    except Exception as e:
        log(" - Executing {}... Error", "INFO", True)
        log("    - {}".format(e), "ERROR", True)
