# GAN-Inference

## To run the app

### Step 1

``` pip install -r requirements.txt ```

### Step 2

``` uvicorn app.api.routes:app --reload ```


## Inference curl request

### Transform request

```
curl -X POST http://localhost:8000/api/v1/transform \
     -H "Content-Type: application/json" \
     -d '{"drive_link": "https://drive.google.com/file/d/1BMZPas2dQI9R4hvUQ6v6Sxdgjpoak_rj/view?usp=drive_link"}'
```

### Inverse Transform request

```
curl -X POST "http://localhost:8000/api/v1/inverse_transform" \
     -H "Content-Type: application/json" \
     -d "{\"transformed_file_path\": \"insert/your/path/here.csv\"}"
```