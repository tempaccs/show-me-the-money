# Show-Me-The-Money [![Codeship Status for tempaccs/show-me-the-money](https://app.codeship.com/projects/d4b21e10-3ac1-0138-6216-72327eda91a4/status?branch=master)](https://app.codeship.com/projects/386930) [![codecov](https://codecov.io/gh/tempaccs/show-me-the-money/branch/master/graph/badge.svg)](https://codecov.io/gh/tempaccs/show-me-the-money)

![alt text](https://media.giphy.com/media/9HQRIttS5C4Za/giphy.gif)

### Build
```bash
docker-compose build
```

### Run
```bash
docker-compose up
```
You can access the server on http://localhost:8000.

### Tests
```bash
docker-compose run web python manage.py test
```

### Endpoints
See http://localhost:8000/redoc.

### Authentication
docker automaticly creates you a user:
- username: `admin`
- password: `welcome`

These credentials can be used for basic auth.

You may create more user with 
```
docker-compose run web python manage.py createsuperuser
```
or via localhost:8000/admin.


### Things to improve
- GitHub flows etc
- descriptions for model fields
- testing the validation error in `transactions` doesnt work, even though it works in practice
- tests in `transaction` and `customers` should test directly the views, not via the URL
- depending on the requirements, maybe Customer model should be replaced by the User model
