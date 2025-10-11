# Movie-Search
Movie Search System with Statistics and Logging

Getting Started
Follow these instructions to get a local copy of the project up and running on your machine for development and testing purposes.

Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.8+

Git

An active MySQL server instance.

An active MongoDB server instance.

Launch Method
1. Clone the Repository

First, open your terminal, navigate to the directory where you want to store the project, and clone the repository.

Bash

git clone https://github.com/iuriestratulat/Movie-Search.git
cd Movie-Search
2. Create a Virtual Environment

It is a standard best practice to create a virtual environment to keep the project's dependencies isolated from your global Python installation.

On Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
On macOS & Linux:

Bash

python3 -m venv venv
source venv/bin/activate
Your terminal prompt should now indicate that you are in the (venv) environment.

3. Install Dependencies

Install all the required Python packages using the requirements.txt file. This command reads the file and installs the exact versions of the libraries needed for the project.

Bash

pip install -r requirements.txt
4. Configure Local Settings

The application requires credentials to connect to your local MySQL and MongoDB databases. These are stored in a local settings file that you must create.

In the project folder, find the template file named local_settings.py.example.

Create a copy of this file and rename the copy to local_settings.py.

Open local_settings.py with a text editor and fill in your actual database credentials (host, username, password, database name, etc.).

Example local_settings.py:

Python

# Rename this file to local_settings.py and fill in your database credentials.

# --- MySQL Database Settings ---
DB_HOST = "localhost"
DB_USER = "your_mysql_username"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "your_database_name"

# --- MongoDB Settings (for logging stats) ---
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "logs_db"
Important: The local_settings.py file is intentionally ignored by Git (via .gitignore) to ensure that your sensitive credentials are never published to GitHub.

5. Run the Application

Once the setup is complete, you can launch the main application script from your terminal:

Bash

python scripts/main.py
The movie search console interface should now start, and you can begin using the application.
