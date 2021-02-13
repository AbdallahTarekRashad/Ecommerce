# Ecommerce
### for install project 
#### DataBase Install 
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
#### venv install 
```
$ sudo pip install virtualenv 
$ virtualenv -p /usr/bin/python3.8 venv # path to python interprater python3.
$ source venv/bin/activate
$ pip install -r requirements.txt
```
#### Project Run
```
$ python manage.py createsuperuser #create superuser to use in project
$ python manage.py runserver
```
#### jet Errors
jet admin dashboard use `admin_static` in template and use some function from django2 but in this project using django3 and change it after install if not work with you just remove it from settings.py `INSTALLED_APPS`


#### AdminLte Dashboard
http://127.0.0.1:8000/seller/
