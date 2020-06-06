# HW5

This homework was done on mac OS, so some commands are specific for this system.

Install brew (package manager):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

Install postgres:
pip install postgres

Install psql:
brew install psql

Run DB:
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql

Create new user:
createuser <username>

Create DB (name "models"):
createdb models

Username and db name your can config in local "config.json" file that should be in the same directory as HW5.ipynb jup. notebook. 
Structure of "config.json" file:
```
{
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': '<username>',
    'password': 'admin',
    'database': 'models'
}
```
