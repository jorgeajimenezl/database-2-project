# Computer Science Database II Project
Flask web app to manage some random truck company and theirs travels.

## Deploy
First at all, create some virtual enviroment to install all dependencies
```shell
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```shell
export FLASK_APP='app.wsgi'
export FLASK_ENV='development'
export SQLALCHEMY_DATABASE_URI='mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4'
```

Then run the migrations
```shell
flask db init
flask db migrate
flask db upgrade
```

Finally, run the app
```shell
flask run
```

## Authors
+ Livan Rafael Arzuaga Sanchéz <<livanarzuaga@gmail.com>>
+ Jorge Alejandro Jiménez Luna <<jorgeajimenezl17@gmail.com>>