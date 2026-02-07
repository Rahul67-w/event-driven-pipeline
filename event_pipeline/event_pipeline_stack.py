from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3_notifications as s3n,
)
from constructs import Construct

class EventPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self, "EventsTable",
            partition_key=dynamodb.Attribute(
                name="event_id",
                type=dynamodb.AttributeType.STRING
            )
        )

        fn = _lambda.Function(
            self, "ProcessorFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="processor.handler",
            code=_lambda.Code.from_asset("lambda/processor"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        table.grant_write_data(fn)

        bucket = s3.Bucket(self, "IncomingBucket")
        bucket.grant_read(fn)

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(fn)
        )