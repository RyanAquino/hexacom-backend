# Hexacom API

## Endpoints
1. Users
    - `POST - /login:` Authenticate User
    - `POST - /register:` Register a user
    - `GET - /users:` Retrieve all users 
    - `GET - /user/<username>:`  Retrieve a user
    - `DELETE - /user/<username>:` Delete a user

2. Brands
   - `GET - /brands:` Retrieve all brands
   - `GET - /brand/<name>:` Retrieve a brand
   - `POST - /brand/<name>:` Create a brand
   - `DELETE - /brand/<name>:` Delete a brand

3. Job Orders
    - `GET - /job_orders:` Retrieve all job orders
    - `GET - /job_order/generate_uid:` Generate a job order ID
    - `GET - /job_order/<uid>:` Get a job order
    - `POST - /job_order/<uid>:` Create a job order
    - `DELETE - /job_order/<uid>:` Delete a job order

Swagger documentation: `/swagger`

## Setup

### with Docker
#### Change the database URI to the value below:
```
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin@db/hexacom"
```

#### Start the docker application
```
docker-compose up
```

### without Docker
#### Create virtual environment

```
virtualenv venv
```
#### Install dependencies

```
pip install -r requirements.txt
```
#### Initialize database and apply the latest migration
```
flask admin db_init
```
#### Populate the database with test data. 
```
flask seeder all
```
#### Removing the test data
```
flask seeder all --remove
```
Note: You may replace `all` with specific table. More options can be found using
`flask seeder` command.
#### Create an admin user using the command line
```
flask admin create_admin_user
```

Note: You may view more commands using `flask admin`.

#### Starting the application
```
python app.py
```



