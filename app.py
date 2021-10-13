from flask import Flask, render_template, request
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient
import redisOperations
import redis
from datetime import datetime
#import os
#import cmd
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import uuid

endpoint = "https://bdt2021email.documents.azure.com:443/"
key = 'zQeLqb6v31n2Rlcb1KZHxdoiypuoKQ1uxeU0wcMhI4vjqLEKfSrmgqlRIJ8e8mWi8q0VKpzqurAPxrtEeNWYWQ=='

""" from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

KVUri = f"https://redikey.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

retrieved_secret = client.get_secret("rediskey") """

hostname = 'bdt2021.redis.cache.windows.net'
#access = retrieved_secret.value
access = 'm47NcmWesLSpCwA2DagnRuCVFnrevw5YImMkFSfGgnM='
r = redis.StrictRedis(host=hostname,
        port=6380, db=0, password=access, ssl=True)

#CONNECTION_STR = "Endpoint=sb://bdt2021.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=+4MIsktdwEvSwVBUZ5a5x8ro3i5cYbyZR27J+K0bqko="
#TOPIC_NAME = "btc_pred"
#SUBSCRIPTION_NAME = "sb_mgmt_subc27ff570-9723-4b32-bf6d-1a5d604a5e57"
#
# create a Service Bus client using the connection string
#servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)

# app = Flask(__name__)

# @app.route("/")
# def hello():
#     mess = ""
    # with servicebus_client:
    # # get the Subscription Receiver object for the subscription    
    #     receiver = servicebus_client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5)
    #     with receiver:
    #         for msg in receiver:
    #             mess = str(msg)
    #             print("Received: " + str(msg))
    #             # complete the message so that the message is removed from the subscription
    #             #receiver.complete_message(msg)
    # return mess

# with servicebus_client:
#     # get the Subscription Receiver object for the subscription    
#     receiver = servicebus_client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5)
#     with receiver:
#         for msg in receiver:
#             mess = str(msg)
#             print("Received: " + str(msg))

app = Flask(__name__)


@app.route('/', methods =['GET','POST'])
def home():
    msg = "Subscribe to email list to receive daily report at midnight."
    col = "black"
    email = request.form.get('email')
    if(email):
        client = CosmosClient(endpoint, key)
        database_name = 'emails'
        database = client.create_database_if_not_exists(id=database_name)
        container_name = 'emails'
        container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
        )
        query = "SELECT * from c WHERE c.email='{}'".format(email)
        items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
        ))
        if(len(items)==0):
            item = {'id':str(uuid.uuid4()),'email':email}
            container.create_item(body=item)
            msg = "SUCCESS: E-mail saved to the db."
            col = "green"
            print(msg)
        else:
            msg = "ERROR: Email already exists in the db."
            col = "red"
            print(msg)
        
#    key, mess = redisOperations.getLastValue(r)
#    mess = str(mess)
#    last_update = datetime.fromtimestamp(key).strftime("%Y-%m-%d %H:%M:%S")
    l_preds = redisOperations.getLastPreds(r)
    last_update, mess = l_preds[-1]
    hex = "gray"
    t_color = "gray"
    signal = "No Signal"
    if(mess=="Buy"):
        hex = 'green'
        t_color = '#009879'
        signal = "Buy Bitcoin"
    if(mess=="Sell"):
        hex = 'red'
        t_color = '#720505'
        signal = "Sell Bitcoin"
    return render_template('index.html', hex = hex, signal = signal, last_update = last_update, l_preds = l_preds, t_color = t_color, msg=msg, col=col)

@app.route('/unsub', methods =['GET', 'POST'])
def unsub():
    unsub_email = request.args.get("unsub_email")
    client = CosmosClient(endpoint, key)
    database_name = 'emails'
    database = client.create_database_if_not_exists(id=database_name)
    container_name = 'emails'
    container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
    )
    if(unsub_email):
        query = "SELECT * from c WHERE c.email='{}'".format(unsub_email)
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
            ))
        if(len(items)>0):
            for item in items:
                container.delete_item(item = item['id'], partition_key=item['id'])
                return """<h1>{0} subscription successfully deleted.</h1>""".format(unsub_email)
        else:
            return """<h1>ERROR: No subscription found belonging to {0}</h1>""".format(unsub_email)
    else:
        return """<h1>ERROR: You are not supposed to be here.</h1>"""

if __name__ == '__main__':
    app.run(debug=True)

