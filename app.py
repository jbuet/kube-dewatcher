from kubernetes import client, config, watch
from pprint import pprint
from kubernetes.client.rest import ApiException
import time
import sys

try:
    config.load_incluster_config()
except Exception as e:
    print ("Exception when loading kubernetes configuration: %s\n" % e, flush=True)
    sys.exit(1)

v1 = client.AppsV1Api()
print("Listing deployments status")
while True:
    ret = v1.list_deployment_for_all_namespaces(watch=False)
    for i in ret.items:
        for e in i.status.conditions:
            if e.status == 'False':
                print("Deployment %s at namespace %s have failed. Reason: %s" % (i.metadata.name,i.metadata.namespace, e.reason), flush=True)

    time.sleep(30)