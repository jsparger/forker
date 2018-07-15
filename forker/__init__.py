from flask import Flask
from flask_restful import reqparse, Resource, Api
import sqlite3
import types
import os
from forker.db import init_app, get_db
import json

app = Flask(__name__)
api = Api(app)

app.config.from_mapping(
    DATABASE=os.path.join(app.instance_path, 'forker.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(api_route, api)

parser = reqparse.RequestParser()
parser.add_argument('content')

@api.route("/commit/<id>")
class Commit(Resource):
    def get(self, id):
        db = get_db()
        query = 'SELECT id,parent,content FROM version v WHERE v.id=?;'
        print(query)
        commit = db.execute(query, (id,)).fetchone()
        print({"id": commit[0], "parent": commit[1], "content": commit[2]})
        return {"id": commit[0], "parent": commit[1], "content": json.loads(commit[2])}

    def post(self, id):
        parent_id = id
        args = parser.parse_args()
        try:
            parent = self.get(parent_id)
        except Exception as e:
            return ("Parent commit ID not valid", 400)
        try:
            content = args["content"]
            validate = json.loads(content);
        except ValueError:
            return ("Content is not valid JSON", 400)
        if (validate == parent["content"]):
            return ("Content has not changed. Nothing to commit", 400)
        db = get_db()
        db.execute(
            'INSERT INTO version (parent, content)'
            ' VALUES (?, ?);',
            (parent_id, content)
        )
        db.commit()
        new_id = db.execute(' SELECT last_insert_rowid();').fetchone()[0]
        return (self.get(new_id), 201)

init_app(app)
