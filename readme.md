## Marcus

A movie & music review application built around the TMDB & Spotify APIs

## Documentation

- [View Swagger](https://app.swaggerhub.com/apis-docs/ARTHMAYER/Marcus-API/1.0.0)

- [View Yaml](./specification.yml)

## Technologies used

|Usage|Name|Version|
|-|-|-|
|Language|Python|3.11.0
|Framework|Django|4.2.2
|TMDB API|tmdbsimple|2.9.1
|CORS Library|django-cors-headers|3.13.0
|REST Library|djangorestframework|3.14.0
|JWT Library|djangorestframework-simplejwt|5.2.2

## Usage

- Clone the repo
```bash
git clone https://github.com/Zararthustra/marcus_back
```

- Install dependencies
```bash
pip install -r requirements.txt
```

- Make database migration (in `src`)
```bash
python manage.py makemigrations marcus marcus_music
```
```bash
python manage.py migrate
```

- Run tests (in `src`)
```bash
python manage.py test marcus marcus_music --verbosity=2
```

- Run server (in `src`)
```bash
python manage.py runserver 0.0.0.0:8000
```