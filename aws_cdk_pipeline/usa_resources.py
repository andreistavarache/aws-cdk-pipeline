from aws_cdk import (
    Environment,
    RemovalPolicy,
    Stage,
    Duration,
    Stack,
    aws_ecs as ecs,
    aws_sqs as sqs,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2
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
        vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        alb_sg = ec2.SecurityGroup(self, "SecurityGroup1", 
                                   security_group_name="alb-sg",
                                   vpc=default_vpc,
                                   allow_all_outbound=True,
                                   )
        ecs_sg = ec2.SecurityGroup(self, "SecurityGroup2", 
                                   security_group_name="ecs-sg",
                                   vpc=default_vpc,
                                   allow_all_outbound=True,
                                   )
        alb_sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), 
                                connection=ec2.Port.tcp(80), 
                                description="allow http access from the world")
        ecs_sg.add_ingress_rule(peer=ec2.Peer.security_group_id(alb_sg.security_group_id), 
                                connection=ec2.Port.tcp(80), 
                                description="allow http access from the world")
        

        alb = elbv2.ApplicationLoadBalancer(self, "ALB", 
                                            vpc=default_vpc, 
                                            internet_facing=True,
                                            security_group=alb_sg
                                            )
        listener = alb.add_listener("Listener", port=80)

        
        cluster = ecs.Cluster(self, "Cluster", 
                              cluster_name="ecs-cluster",
                              container_insights=True,
                              enable_fargate_capacity_providers=True,
                              vpc=default_vpc)
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef")

        task_definition.add_container("web",
                                      container_name="nginx-example",
                                      image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                                      port_mappings=[ecs.PortMapping(container_port=80)]
                                      )
        service=ecs.FargateService(self, "FargateService",
                                   service_name="fargate-service",
                                   cluster=cluster,
                                   task_definition=task_definition,
                                   security_groups=[ecs_sg],
                                   desired_count=2
                                   # vpc_subnets=vpc_subnets
                                )
        target_group = listener.add_targets("ECS1",
                                            port=80,
                                            targets=[service]
                                        )

class DeployUSAStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ResourceUSAStack(self, 'ResourceStack', env=env, stack_name='test-stack-in-USA')