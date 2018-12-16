class SecretRef:
    namespace: str
    name: str

    user_ref: str
    password_ref: str

    def __init__(self, obj):
        self.namespace = obj["namespace"]
        self.name = obj["name"]
        self.password_ref = None
        self.user_ref = None
        if "userRef" in obj: self.user_ref = obj["userRef"]
        if "passwordRef" in obj: self.password_ref = obj["passwordRef"]

class ServerDefinition:
    host: ""
    secret: SecretRef

    def __init__(self, obj):
        self.host = obj["host"]
        self.secret = SecretRef(obj["secret"])


class Spec:
    def __init__(self, obj):
        self.server = ServerDefinition(obj["server"])
        self.user = MongoDbUser(obj["user"])


class MongoDbUser:
    secret: SecretRef

    def __init__(self, obj):
        self.secret = SecretRef(obj["secret"])

