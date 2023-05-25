import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_pipeline.aws_cdk_pipeline_stack import AwsCdkPipelineStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_pipeline/aws_cdk_pipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdkPipelineStack(app, "aws-cdk-pipeline")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
