from aws_cdk import (
    Environment,
    RemovalPolicy,
    Stage,
    Duration,
    Stack,
    aws_ecs as ecs,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_ec2 as ec2
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
                           bucket_name=f"my-american-bucket-{random_string.lower()}",
                           versioned=True,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           auto_delete_objects=True,
                           removal_policy=RemovalPolicy.DESTROY
                           )
        default_vpc = ec2.Vpc.from_lookup(self, "default-VPC", is_default=True)

        cluster = ecs.Cluster(self, "Cluster", 
                              enable_fargate_capacity_providers=True,
                              vpc=default_vpc)
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef")

        task_definition.add_container("DefaultContainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            memory_limit_mib=512
        )

        # Instantiate an Amazon ECS Service
        ecs_service = ecs.FargateService(self, "Service", cluster=cluster, task_definition=task_definition)


class DeployUSAStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ResourceUSAStack(self, 'ResourceStack', env=env, stack_name='test-stack-in-USA')