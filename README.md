# simple-renting-book-server
Django Simple Renting Book Server

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

