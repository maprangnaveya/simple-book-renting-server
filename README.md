# simple-renting-book-server
Django Simple Renting Book Server

## Development
```shell
docker compose up
```
### Account for local env
email: dev@mockupemail.com
password: random-user-pass!

### URLs
1. [localhost:8000:/admin/](http://localhost:8000/admin/): Django admin
2. [localhost:8000:/api-explorer/](http://localhost:8000/api-explorer/): Django API explorer


## Import books data

1. Import by static file
```shell
docker exec -it {web_container} bash
python manage.py load_books_from_openlibrary_static_file book_manager/books-sherlock-holmes.json 
```

2. Import by request books from openlibrary API
```shell
docker exec -it {web_container} bash
python manage.py load_books_from_openlibrary
```


## TODO

- [ ] Available Books API
- [ ] User's Renting Logs API
- [ ] Add tags to Book model
- [ ] Add description to Book model
- [ ] Import books data via Django admin button
- [ ] Setup MailCatcher to test send email on local env
- [ ] Scheduled task send email reminder user when the due date(return date) less than x days
- [ ] Scheduled task send email reminder renting is overdue
- [ ] Unit testing
