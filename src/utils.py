from base64 import b64decode

from kubernetes.client import CoreV1Api

from src.models import SecretRef


def get_username_password(ref: SecretRef, api: CoreV1Api):

    secret = api.read_namespaced_secret(namespace=ref.namespace,
                                                 name=ref.name,
                                                 exact=True,
                                                 export=True)

    raw = None

    if ref.password_ref is not None:
        raw = secret.data[ref.password_ref]
    elif "mongodb-root-password" in secret.data:
        raw = secret.data["mongodb-root-password"]
    elif "mongodb-password" in secret.data:
        raw = secret.data["mongodb-password"]
    elif "password" in secret.data:
        raw = secret.data["passsword"]

    if raw is None:
        raise RuntimeError("Invalid secret, must have key mongodb-root-password, mongodb-password or passsword")

    password = b64decode(raw).decode("utf-8")
    raw = None

    if ref.user_ref is not None:
        raw = secret.data[ref.user_ref]
    if "mongodb-root-user" in secret.data:
        raw = secret.data["mongodb-root-user"]
    elif "mongodb-user" in secret.data:
        raw = secret.data["mongodb-user"]
    elif "user" in secret.data:
        raw = secret.data["user"]

    if raw is None:
        return (None, password)
        # raise RuntimeError("Invalid secret, must have key mongodb-root-user, mongodb-user or user")
    user = b64decode(raw).decode("utf-8")
    return (user, password)