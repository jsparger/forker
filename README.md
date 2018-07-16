# forker

### to install:

```
git clone https://github.com/jsparger/forker.git
cd forker
git checkout absolute-minimum
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### to run:

```
export FLASK_APP=forker
export FLASK_ENV=development
flask init-db # do this before running the app the first time
flask run
```

### usage

##### get the root commit:

```
curl -i -X GET localhost:5000/commit/0
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 52
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Sun, 15 Jul 2018 22:43:00 GMT

{
    "id": 0,
    "content": {},
    "parent": 0
}


```

##### create a new commit (id=1) based on the root commit (id=0)

```
curl -i -X POST localhost:5000/commit/0 -d 'content={"dog": 7}'
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 74
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Sun, 15 Jul 2018 22:43:25 GMT

{
    "id": 1,
    "content": {
        "dog": 7
    },
    "parent": 0
}
```

##### get the new commit:

```curl -i -X GET localhost:5000/commit/1
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 74
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Sun, 15 Jul 2018 22:44:32 GMT

{
    "id": 1,
    "content": {
        "dog": 7
    },
    "parent": 0
}

```


##### try to create a new commit without changing content:

```
curl -i -X POST localhost:5000/commit/1 -d 'content={"dog": 7}'
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Sun, 15 Jul 2018 22:45:52 GMT

"Content has not changed. Nothing to commit"
```

##### try to create a new commit with something other than valid JSON as content

```
curl -i -X POST localhost:5000/commit/1 -d 'content=[something else]'
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 28
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Sun, 15 Jul 2018 22:47:54 GMT

"Content is not valid JSON"
```

##### try to create a new commit with a nonexisting parent commit
```
curl -i -X POST localhost:5000/commit/999 -d 'content={"dog": 9}'
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 29
Server: Werkzeug/0.14.1 Python/3.5.2
Date: Sun, 15 Jul 2018 22:50:31 GMT

"Parent commit ID not valid"
```
