Here is the information written in Markdown format:

# accuknox-task
=====================

Getting Started
---------------

### Create Virtual Environment
Run the following command in your terminal:
```python -m venv myenv```
Replace `myenv` with the name you want to give your virtual environment.

### Activate Virtual Environment
Activate the virtual environment using the following command:
```
myenv\Scripts\activate (on Windows) or source myenv/bin/activate (on macOS/Linux)
```
This will activate the virtual environment, and your terminal should indicate that you're now working within it.

### Install Dependencies
Install the dependencies listed in `requirements.txt` using pip:
```
pip install -r requirements.txt
```

Running the App
---------------

Move to the directory that contains the manage.py file
```
cd src/social_network
```

### Run Migrations
Run the following command to apply migrations:
```
python manage.py makemigrations
python manage.py migrate
```

### Create Super User
Run the following command to create super user for the app:
```
python manage.py createsuperuser
```

### Start Development Server
Start the development server using the following command:
```
python manage.py runserver
```
This will start a development server at `http://localhost:8000/`. You can access the api's using postman or through the browser

### Run Docker Compose
If you're using Docker, you can run the following command in the root directory instead of starting the dev server using the command mentioned above
to start the containers: 
```
docker-compose build 
```

```
docker-compose up -d 
```

This will start the containers in detached mode. You can then access your app by visiting http://localhost:8000/ in your web browser. Only run the docker commands after creating the super user and running migrations.



Other Commands
---------------

* To run tests, use: `python manage.py test`