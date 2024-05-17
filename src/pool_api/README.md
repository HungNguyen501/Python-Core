DE Homework
-----------------------

# Deployment
```bash
docker compose up
```

# API methods:
> Host: **0.0.0.0:8501**

**First API**
----
  Returns status of the pool action.

* **URL:** /upsert

* **Method:** `POST`

* **Data Params**

  ```json
  {
    "pool_id": 1, //integer,
    "values": [1, 2] //[integer]
  }
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json
    {
        "status": "appended" //or "inserted"
    }
    ```


  OR

  * **Code:** 422 Unprocessable Entity <br />
    **Content:**
    ```json
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "pool_id"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }
    ```

**Second API**
----
  Returns statistics of a pool_id.

* **URL:** /statistics

* **Method:** `POST`

* **Data Params**

  ```json
  {
    "pool_id": 1, //integer
    "percentile": 99.5 //float number in range [1, 100]
  }
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
    ```json
    {
        "quantile_value": 99, //numeric number
        "total account": 9 // integer
    }
    ```


  OR

  * **Code:** 422 Unprocessable Entity <br />
    **Content:**
    ```json
    {
        "detail": [
            {
                "loc": [
                    "body",
                    "pool_id"
                ],
                "msg": "value is not a valid integer",
                "type": "type_error.integer"
            }
        ]
    }
    ```

  * **Code:** 400 Bad Request <br />
    **Content:**
    ```json
    {"detail": "Not found pool_id"}
    /*or*/
    {"detail": "Percentile must be in range [0, 100]"}
    ```
