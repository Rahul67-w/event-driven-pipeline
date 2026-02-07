import boto3
from datetime import datetime, timedelta
import csv
import io
import os

def handler(event, context):
    dynamodb = boto3.client('dynamodb')
    s3 = boto3.client('s3')

    table_name = os.environ['TABLE_NAME']
    bucket_name = os.environ['REPORT_BUCKET']

    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')

    response = dynamodb.scan(TableName=table_name)
    count = len(response.get('Items', []))

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['date', 'event_count'])
    writer.writeheader()
    writer.writerow({'date': yesterday, 'event_count': count})

    s3.put_object(
        Bucket=bucket_name,
        Key=f'reports/daily-summary-{yesterday}.csv',
        Body=output.getvalue()
    )

    return {"statusCode": 200}