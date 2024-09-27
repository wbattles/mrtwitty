from flask import Flask, jsonify
import os
import boto3
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)

aws_region = os.getenv('AWS_DEFAULT_REGION')
db_name= os.getenv('DYNAMO_DB_NAME')

dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table = dynamodb.Table(db_name)

@app.route('/')
def home():
    return "Hello darlin"

@app.route('/track/<track_id>', methods=['GET'])
def get_track(track_id):
    response = table.get_item(Key={'track_id': track_id})
    return jsonify(response['Item'])


@app.route('/track/name/<track_name>', methods=['GET'])
def get_track_name(track_name):
    response = table.scan(FilterExpression=Attr('track_name').contains(track_name))
    return jsonify(response['Items'])


@app.route('/album/<album_name>', methods=['GET'])
def get_album_name(album_name):
    response = table.scan(FilterExpression=Attr('album_name').contains(album_name))
    return jsonify(response['Items'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)