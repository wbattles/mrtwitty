import boto3
import json
import os

dynamodb = boto3.resource("dynamodb")

db_name= os.getenv('DYNAMO_DB_NAME')
table = dynamodb.Table(db_name)

with table.batch_writer() as batch:
    with open("conway_info.json", "r") as json_file:
        data = json.load(json_file)
    
    for item in data:
        batch.put_item(Item=item)