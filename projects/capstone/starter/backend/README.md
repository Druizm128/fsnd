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

# Test DB

```
createdb test_talentagency
```

# API Documentation

`GET '/actors`

* Fetches a dictionary of actors in which the keys are the name and the age and the gender.

* **Request Arguments:** None

* **Returns:** An object with a single key, categories, that contains an object of id: category_string key: value pairs.

    ```json
    {
        "actors": [
            {
                "age": 58,
                "gender": "M",
                "id": 3,
                "name": "Robert Downey Jr."
            },
            {
                "age": 58,
                "gender": "M",
                "id": 4,
                "name": "Robert Downey Jr."
            },
            {
                "age": 58,
                "gender": "M",
                "id": 5,
                "name": "Robert Downey Jr."
            }
        ],
        "success": true
    }
    ```

`DELETE '/actors/<int:id>'`

* Deletes an actor using the actor ID. 
  
* **Request Arguments:** 
  - `id`(int)

* **Returns:** Returns a JSON object with keys delete id, and success status.


    ```json
    {
        "delete": 3,
        "success": true
    }
    ```

`POST '/actors'`

* Posts a new actor.

* **Request Arguments:**  Does not require an argument. Requires the body JSON object with title (`str`) and release date (`int`) in the `YYYY` format.

    ```json
    {
        "name": "Robert Downey Jr.",
        "age": "58",
        "gender": "M"
    }
    ```

* **Returns:** An object with a single key, actor, that contains a JSON object with the `age`, `gender`, `id` and `name`.


    ```json
    {
        "actor": [
            {
                "age": 58,
                "gender": "M",
                "id": 6,
                "name": "Robert Downey Jr."
            }
        ],
        "success": true
    }
    ```

`PATCH '/actors/<int:id>'`

* Update an existing actor.

* **Request Arguments:**  Requires to pass an argument of the actor database `id` (`int`). Also requieres a JSON body object with the updates on the `title` and `release_date` of the movie (`YYYY`).

    ```json
    {
        "name": "Robert Downey Jr. (The One and Only)",
        "age": "58",
        "gender": "M"
    }
    ```

* **Returns:** An object with a single key, movie, that contains an object with `id`, `age`, `name` and `gender`.


    ```json
    {
        "actor": [
            {
                "age": 58,
                "gender": "M",
                "id": 3,
                "name": "Robert Downey Jr. (The One and Only)"
            }
        ],
        "success": true
    }
    ```

`GET '/movies'`

* Fetches a dictionary of movies in which the keys are the title and the release date.

* **Request Arguments:** None

* **Returns:** An object with a single key, categories, that contains an object of id: category_string key: value pairs.


    ```json
    {
        "movies": [
            {
                "id": 2,
                "release_date": "2008",
                "title": "The Incredible Hulk"
            },
            {
                "id": 3,
                "release_date": "2018",
                "title": "Avengers: Infinity War"
            },
            {
                "id": 4,
                "release_date": "2008",
                "title": "The Incredible Hulk"
            },
            {
                "id": 5,
                "release_date": "2008",
                "title": "The Incredible Hulk"
            }
        ],
        "success": true
    }
    ```

`DELETE '/movies/<int:id>'`

* Deletes a movie using the movie ID. 
  
* **Request Arguments:** 
  - `id`(int)

* **Returns:** Returns a JSON object with keys delete id, and success status.


    ```json
    {
        "delete": 3,
        "success": true
    }
    ```

`POST '/movies'`

* Posts a new movie.

* **Request Arguments:**  Does not require arguments just a JSON body with title (`str`) and release date (`int`) in the `YYYY` format.

    ```json
    {
        "title": "The Incredible Hulk",
        "release_date": 2008
    }
    ```

* **Returns:** An object with a single key, movie, that contains an object with `id`, `release_date` and `title`.


    ```json
    {
        "movie": [
            {
                "id": 7,
                "release_date": "2008",
                "title": "The Incredible Hulk"
            }
        ],
        "success": true
    }
    ```

`PATCH '/movies/<int:id>'`

* Update an existing movie.

* **Request Arguments:**  Requires to pass an argument of the movie database `id` (`int`). Also requieres a body JSON object with the updates on the `title` and `release_date` of the movie (`YYYY`).

    ```json
    {
        "title": "The Incredible Hulk",
        "release_date": 2008
    }
    ```

* **Returns:** An object with a single key, movie, that contains an object with `id`, `release_date` and `title`.


    ```json
    {
        "movie": [
            {
                "id": 3,
                "release_date": "2008",
                "title": "The Incredible Hulk (Marvel)"
            }
        ],
        "success": true
    }
    ```