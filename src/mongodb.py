from kubernetes.client import CoreV1Api
from pymongo import MongoClient

from src.models import Spec
from src.utils import get_username_password


def get_mongo_connection_string(password: str, spec: Spec):

    host = spec.server.host
    user = "admin"
    return "mongodb://" + user + ":" + password + "@"+ host


def get_admin_db(connection_str):
    client = MongoClient(connection_str)
    return client.admin


def create_user(spec: Spec, api: CoreV1Api):

    [unused, root_password] = get_username_password(spec.server.secret, api)

    connection_str = get_mongo_connection_string(root_password, spec)

    (username, password) = get_username_password(spec.user.secret, api)

    db = get_admin_db(connection_str)

    db.command("createUser", username, pwd=password, roles=["root"])
