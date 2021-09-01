# Example API interaction with the PostgreSQL-based application

1. Create a new entry:

```bash
$ curl -d '{"name": "Carol", "fav_dish": "SPAM Bruschetta"}' \
    -H "Content-Type: application/json" \
    -X POST \
    http://localhost:8000/patron
{"msg": "ok", "id": 37}
```

2. Read an entry
```bash
$ curl -X GET http://localhost:8000/patron/37
{"id":37, "name":"Carol", "fav_dish":"SPAM Bruschetta"}
```

3. Update entry
```bash
$ curl -d '{"name": "Eric", "fav_dish": "SPAM Bruschetta"}' \
    -H "Content-Type: application/json" \
    -X PUT \
    http://localhost:8000/patron/37
# Get the updated entry
$ curl -X GET http://localhost:8000/patron/37
{"msg":"ok"}
{"id":37,"name":"Eric","fav_dish":"SPAM Bruschetta"}
```

4. Delete an entry
```bash
$ curl -X DELETE http://localhost:8000/patron/37
$ curl -X GET http://localhost:8000/patron/37
{"msg":"ok"}
null
```
