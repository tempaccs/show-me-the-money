# Show-Me-The-Money

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

### Things to improve
- CI, GitHub flows etc
- descriptions for model fields
- testing the validation error in `transactions` doesnt work, even though it works in practice
- tests in `transaction` and `customers` should test directly the views, not via the URL
- depending on the requirements, maybe Customer model should be replaced by the User model
