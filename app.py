
import os

import aws_cdk as cdk

from event_pipeline.event_pipeline_stack import EventPipelineStack


app = cdk.App()
EventPipelineStack(app, "EventPipelineStack")
app.synth()
