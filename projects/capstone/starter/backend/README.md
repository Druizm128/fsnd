# Set up and Populate the Database

```
createdb talentagency
```


```
psql talentagency < talentagency.psql
```

# Run API

```bash
FLASK_APP=app.py 
FLASK_DEBUG=true 
flask run --reload
```