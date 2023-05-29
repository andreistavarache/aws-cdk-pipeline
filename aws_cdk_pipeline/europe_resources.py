from aws_cdk import (
    Environment,
    RemovalPolicy,
    Stage,
    Duration,
    Stack,
    pipelines as cdkpipe,
    aws_codepipeline as pipe,
    aws_sqs as sqs,
    aws_s3 as s3
)
from constructs import Construct
import random, string


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

random_string = generate_random_string(10)

class ResourceEuropeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "MyEuropeanQueue",
            visibility_timeout=Duration.seconds(300),
        )
        bucket = s3.Bucket(self, "myEuropeanBucket", 
                        bucket_name=f"my-european-bucket-{random_string.lower()}",
                        versioned=True,
                        block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                        auto_delete_objects=True,
                        removal_policy=RemovalPolicy.DESTROY
                        )
        
class DeployEuropeStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ResourceEuropeStack(self, 'ResourceStack', env=env, stack_name='test-stack-in-EUROPE')
