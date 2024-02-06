# simple-renting-book-server
Django Simple Renting Book Server

## Import books data

```shell
docker exec -it {web_container} bash
python manage.py load_books_from_openlibrary_static_file book_manager/books-sherlock-holmes.json 
```

