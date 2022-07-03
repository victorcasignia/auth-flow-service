# Installation

The application is built using `docker-compose`. Install docker-compose from https://docs.docker.com/compose/install/.

Database will be automatically created and migrated during startup. Make sure the ports `3000`, `5432` and `8000` are available.

Build and run the application by using the command:

    docker-compose build
    docker-compose up

# Usage

Application can be accessed on http://localhost:3000. This include the sign-up, login and dashboard pages.

API can be accessed on http://localhost:8000. All routes except `api/login` and `api/signup` requires auth. To get access token, use the `api/signup` endpoint, take the `access_token` attribute and attach the token to the authorization header as `Bearer {token_here}`.

API documentation is available through the endpoint `http://localhost:8000/swagger`. ERD is within the backend source code as a png file. Endpoints return a JSON representation of the model accessed, for list endpoints a JSON array containing the data is returned.

# Database loading

To load the database dump included in this repository, run the following command:

    docker-compose exec backend python manage.py loaddata data_dump.json

# Unit tests

To run unit tests, run the following command:

    docker-compose exec backend python manage.py test