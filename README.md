# Ecommerce
### for install project 
#### DataBase Install: 
##### Postgres (Default DataBase)
```sql
sudo -u postgres psql
CREATE DATABASE ecommerce;
CREATE USER ecommerce WITH PASSWORD '123456';
ALTER ROLE ecommerce SET client_encoding TO 'utf8';
ALTER ROLE ecommerce SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ecommerce;
ALTER USER ecommerce WITH SUPERUSER;
```
##### Sqlite
you should change in `settings.py` `DATABASES.default.ENGINE` to `django.db.backends.sqlite3`
#### venv install :
```commandline
$ sudo pip install virtualenv 
$ virtualenv -p /usr/bin/python3.8 venv # path to python interprater python3.
$ source venv/bin/activate
$ pip install -r requirements.txt
```
#### Periodic Tasks
for run periodic tasks daily 
```
$ crontab -e # append this line in last of the file
$ 0 0 */1 * * source dir/to/venv/bin/activate; python dir/to/project/Ecommerce/manage.py runcrons
```
#### Project Run:
```commandline
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py add_countries # for fill country tabel from country.json 
$ python manage.py createsuperuser # create superuser to use in project
$ sudo docker run -p 6379:6379 -d redis:5 # for running redis server for websockets(channels layer) 
$ python manage.py runserver
```
#### jet Errors:
jet admin dashboard use `admin_static` in template and use some function from django2 but in this project using django3 and change it after install if not work with you just remove it from settings.py `INSTALLED_APPS` `'jet',
    'jet.dashboard'`


#### AdminLte Dashboard:
http://127.0.0.1:8000/seller/
#### Api Documentation with (ReDoc)
http://127.0.0.1:8000/api/doc/redoc/
#### Api Schema (.json)
http://127.0.0.1:8000/api/doc/schema.json
#### Api Schema (.yaml)
http://127.0.0.1:8000/api/doc/schema.yaml
#### Deployed Website (above links work with Deployed Website):
http://shopdjango.pythonanywhere.com/
#### Admin Dashboard:
http://shopdjango.pythonanywhere.com/seller/ \
to access functionality of seller admin dashboard log with this username and password
```commandline
username: seller
email: seller@ecommerce.com
password: admin123456
```
