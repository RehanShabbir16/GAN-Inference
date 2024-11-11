# GAN-Inference

## To run the app

### Step 1

``` pip install -r requirements.txt ```

### Step 2

``` uvicorn app.api.routes:app --reload ```


## Inference curl request

```
curl -X POST http://localhost:8000/api/v1/transform \
     -H "Content-Type: application/json" \
     -d '{"drive_link": "https://drive.google.com/file/d/1BMZPas2dQI9R4hvUQ6v6Sxdgjpoak_rj/view?usp=drive_link"}'
```