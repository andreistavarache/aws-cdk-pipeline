from aws_cdk import (
    Stage,
    Duration,
    Stack,
    pipelines as cdkpipe,
    aws_codepipeline as pipe,
    aws_sqs as sqs,
    aws_s3 as s3
)
from constructs import Construct


class ResourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # queue = sqs.Queue(
        #     self, "AwsCdkPipelineQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        # bucket = s3.Bucket(self, "MyfirstBucket", 
        #                    versioned=True,
        #                    block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
