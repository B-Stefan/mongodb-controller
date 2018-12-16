import json

import yaml
from kubernetes import client, config, watch
import os

from src.models import Spec
from src.mongodb import create_user

DOMAIN = "mongodb-controller.local"

# Fix bug
from kubernetes.client.models.v1_endpoints import V1Endpoints
def set_subsets(self, subsets):
    if subsets is None:
        subsets = []
    self._subsets = subsets
setattr(V1Endpoints, 'subsets', property(fget=V1Endpoints.subsets.fget, fset=set_subsets))


if __name__ == "__main__":
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
        definition = '/tmp/mongo-user.yml'
    else:
        config.load_kube_config()
        definition = 'mongo-user.yml'
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    v1 = client.ApiextensionsV1beta1Api(api_client)
    current_crds = [x['spec']['names']['kind'].lower() for x in v1.list_custom_resource_definition().to_dict()['items']]
    if 'mongodbuser' not in current_crds:
        print("Creating users definition")
        with open(definition) as data:
            body = yaml.load(data)
        v1.create_custom_resource_definition(body)

    crds = client.CustomObjectsApi(api_client)

    api_instance = client.CoreV1Api(client.ApiClient(configuration))
    print("Waiting for Users to come up...")
    resource_version = ''
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object, DOMAIN, "v1", "users", resource_version=resource_version)
        for event in stream:
            obj = event["object"]
            operation = event['type']
            spec = obj.get("spec")
            if not spec:
                continue
            metadata = obj.get("metadata")
            resource_version = metadata['resourceVersion']
            name = metadata['name']
            print("Handling %s on %s" % (operation, name))
            done = spec.get("review", False)
            if done:
                continue
            userSpec = Spec(obj["spec"])
            create_user(userSpec, api_instance)
