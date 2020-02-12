from kubernetes import client, config, watch
from pprint import pprint
from kubernetes.client.rest import ApiException
import time
import sys
import argparse
import slack
import os

def publishSlack(token, channel, message):
    client = slack.WebClient(token=token)

    response = client.chat_postMessage(
        channel=channel,
        text=message)
    assert response["ok"]
    assert response["message"]["text"] == message

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--namespace', type=str, default=None, help='Only search for deployments on a single namespace')
    parser.add_argument('--seconds', type=int, default=30, help='Loop sleep for n seconds')
    args = parser.parse_args()

    slack_token = os.environ['SLACK_API_TOKEN'] 
    slack_channel = os.environ['SLACK_CHANNEL']
    cluster_name = os.environ['CLUSTER_NAME']

    try:
        ## load config in cluster with a service account
        config.load_incluster_config()

    except config.config_exception.ConfigException:
        ## local testing
        config.load_kube_config()

    except Exception as e:
        print ("Exception when loading kubernetes configuration: %s\n" % e, flush=True)
        sys.exit(1)

    v1 = client.AppsV1Api()
    print("Listing deployments status")
    while True:
        ## get deployments
        if args.namespace: 
            ret  = v1.list_namespaced_deployment(args.namespace)
        else:
            ret = v1.list_deployment_for_all_namespaces(watch=False)

        for i in ret.items:
            ## checks deployment status
            for e in i.status.conditions:
                if e.status == 'False':
                    message = "Cluster %s :: Deployment %s at namespace %s have failed. Reason: %s" % (cluster_name, i.metadata.name,i.metadata.namespace, e.reason)
                    print( message , flush=True)
                    try:
                        publishSlack(slack_token,slack_channel,message)
                    except Exception as e:
                        print (e)

        time.sleep(args.seconds)

if __name__ == "__main__":
    main()