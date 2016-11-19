# L3 portablity app

This webapp allows to lookup phone numbers to see if they are portable on the Level3 voice network

## Deployment Instructions

1. Create an Heroku account
2. Create new app in Heroku (hereafter <appname>
3. link the app to the github repo
4. deploy the app (Deploy Branch)
5. Download the Heroku CLI
6. run: heroku heroku addons:add heroku-postgresql --app <appname>
7. Initialize database schema (see below)
8. Import data


###Initialize database schame (run once when deploying the app)

heroku run python --app <appname>
'''
from web import app, db
from importer import clear_data, count, import_data, create_all
create_all(app,db)
'''

###Clear all Data (run before importing dat):

heroku run python --app <appname>
'''
from web import app, db
from importer import clear_data, count, import_data, create_all
clear_data(app,db)
'''

###Import footprint data:

heroku run python --app <appname>
'''
from web import app, db
from importer import clear_data, count, import_data, create_all
import_data(app,db)
'''

###Check the count of footprint data:

heroku run python --app <appname>
'''
from web import app, db
from importer import clear_data, count, import_data, create_all
count(app)
'''


##Update Footprint Data:

1. export L3 excel file to 'footprint.csv'
2. check-in in github the new version ofr 'footprint.csv'
3. Clear data (see above)
4. import data (see above)

See the following for more information on Heroku, Flask, SQLAlchemy and postgresql

http://blog.y3xz.com/blog/2012/08/16/flask-and-postgresql-on-heroku


##Other notes:

### If the dyno is not created automatically, run the following:
'''
heroku ps:scale web=1 --app isportable
'''

### MacOS mising libraries
On MacOS, some libraries may not be found. create links to them in /opt/local/lib and add the directory to the dynamic library loader. Use the following environment variable:
'''
DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.6/lib;/opt/local/lib;$DYLD_FALLBACK_LIBRARY_PATH
'''

### running local application with remote DB. Get the database_uri and store it in an environment variable:

heroku run python --app <appname>
'''
import os
os.environ['DATABASE_URL']
'''

save the value in a local environment variable:
DATABASE_URL=<valuereturned>