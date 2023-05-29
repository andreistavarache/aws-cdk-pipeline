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
import random, string
from constructs import Construct

def generate_random_string(length):
    # Choose from uppercase letters, lowercase letters, and digits
    characters = string.ascii_letters + string.digits

    # Generate a random string of specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

random_string = generate_random_string(10)

class ResourceUSAStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "MyAmericaQueue",
            visibility_timeout=Duration.seconds(300),
        )
        bucket = s3.Bucket(self, "MyAmericanBucket", 
                           bucket_name=f"MyAmericanBucket-{random_string}",
                           versioned=True,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           auto_delete_objects=True,
                           removal_policy=RemovalPolicy.DESTROY
                           )
        

class DeployUSAStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ResourceUSAStack(self, 'ResourceStack', env=env, stack_name='test-stack-in-USA')