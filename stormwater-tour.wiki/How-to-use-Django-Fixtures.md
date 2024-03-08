## How to populate the database:

If you would like to use the data that was given by OWP, then you should empty out the database.  
The command to empty the database of the tour information and its user information is  
[**python manage.py flush**](https://docs.djangoproject.com/en/1.9/ref/django-admin/#flush)

The next thing we should do is add all the tour information into the database. The command to load the information into the database is  
**python manage.py loaddata test_data.json**

If you would like to use your own fixture(s), save it into the fixtures folder and use the command  
**python manage.py loaddata "your_fixture_name".json**

Django will look at all the "**fixtures**" folders and find **the_fixture_name.json**, and populate the database with the data. 

Now, we need to add the users. This is to prevent us from having to type **python manage.py createsuperuser** every time we flush the database. If you do not have a user account, make one.

The command to add the users is similar to the command for adding the information of the tour and its sites is    
**python manage.py loaddata users.json**

## How to save database information into .json file

The command to pull all the information from the tours use  
**python manage.py dumpdata --format=json tours --indent 4 > tours/fixtures/test_data.json**

The command to pull user information, use  
**python manage.py dumpdata --format=json auth.User --indent 4 > tours/fixtures/users.json**

Be careful that you do not override the **backup_data.json** after a flush. backup_data.json is a safety net if you happen to overwrite the test_data.json. backup_data.json will only be updated if there is new information needed to be added. If you run dumpdata after a flush, there is nothing in the database and the file will be empty. 