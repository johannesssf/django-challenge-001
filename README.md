# Jungle Devs - Django Challenge #001

## Description

**Challenge goal**: The purpose of this challenge is to give an overall understanding of a backend application. You’ll be implementing a simplified version of a news provider API. The concepts that you’re going to apply are:

- REST architecture;
- Authentication and permissions;
- Data modeling and migrations;
- PostgreSQL database;
- Query optimization;
- Serialization;
- Production builds (using Docker).

**Target level**: This is an all around challenge that cover both juniors and experience devs based on the depth of how the concepts were applied.

**Final accomplishment**: By the end of this challenge you’ll have a production ready API.

## Acceptance criteria

- Clear instructions on how to run the application in development mode
- Clear instructions on how to run the application in a Docker container for production
- A good API documentation or collection
- Login API: `/api/login/`
- Sign-up API: `/api/sign-up/`
- Administrator restricted APIs:
  - CRUD `/api/admin/authors/`
  - CRUD `/api/admin/articles/`
- List article endpoint `/api/articles/?category=:slug` with the following response:
```json
[
  {
    "id": "39df53da-542a-3518-9c19-3568e21644fe",
    "author": {
      "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
      "name": "Author Name",
      "picture": "https://picture.url"
    },
    "category": "Category",
    "title": "Article title",
    "summary": "This is a summary of the article"
  },
  ...
]
```
- Article detail endpoint `/api/articles/:id/` with different responses for anonymous and logged users:

    **Anonymous**
    ```json
    {
      "id": "39df53da-542a-3518-9c19-3568e21644fe",
      "author": {
        "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
        "name": "Author Name",
        "picture": "https://picture.url"
      },
      "category": "Category",
      "title": "Article title",
      "summary": "This is a summary of the article",
      "firstParagraph": "<p>This is the first paragraph of this article</p>"
    }
    ```

    **Logged user**
    ```json
    {
      "id": "39df53da-542a-3518-9c19-3568e21644fe",
      "author": {
        "id": "2d460e48-a4fa-370b-a2d0-79f2f601988c",
        "name": "Author Name",
        "picture": "https://picture.url"
      },
      "category": "Category",
      "title": "Article title",
      "summary": "This is a summary of the article",
      "firstParagraph": "<p>This is the first paragraph of this article</p>",
      "body": "<div><p>Second paragraph</p><p>Third paragraph</p></div>"
    }
    ```

## API documentation

Check the API documentation [here](https://johannesssf.github.io/django-challenge-001/api_doc.html).

## How to run for development

### Dependencies

* docker
* docker-compose
* python 3.5+

Follow the steps below to start developing.

1. Clone the repository and _cd_ to it
```
git clone https://github.com/johannesssf/django-challenge-001.git
cd django-challenge-001
```

2. Run the command to install projetc dependencies
```
pip install -r requirements.txt
```

3. Start the postgres container
```
docker-compose -f docker-compose-dev.yml up -d
```
4. Create a file named ".env" into news_api directory and set the following variables:
```
DEBUG=on
DJANGO_SECRET_KEY='your-secret-key-here-=1%#$21&6@vk8=p6uui&5f*s*6!0^'
POSTGRES_USER=postgres
POSTGRES_PASSWORD=challenge
POSTGRES_URL=localhost
```
5. Use this commando to run the tests:
```
python manage.py test
```
6. Migrate the app models and start the Django server to check the API working
```
python manage.py migrate
python manage.py runserver
```
7. Now open your favorite REST app and start to send request to:
```
http://localhost:8000/api/
```

## How to run for production

Follow the steps below to run a production environment.

1. Build and up the environment containers:

```
docker-compose -f docker-compose-prod.yml up
```

2. Migrate the app models:
```
docker container exec django-challenge-001_web_1 python /app/manage.py migrate
```
3. Now open your favorite REST app and start to send request to:
```
http://<server ip address>:8008/api/
```
