from aws_cdk import (
    Stage,
    Duration,
    Environment,
    Stack,
    pipelines as cdkpipe,
    aws_codepipeline as pipe,
)

from constructs import Construct
from .resources import ResourceStack


class DeployStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ResourceStack(self, 'ResourceStack', env=env, stack_name='test-stack-in-other-regions')



class AwsCdkPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_input = cdkpipe.CodePipelineSource.connection(repo_string="andreistavarache/aws-cdk-pipeline",
                                                          branch="main",
                                                          connection_arn="arn:aws:codestar-connections:us-east-1:061515210591:connection/2dfb975c-803a-4935-b3b9-f128cacdb419"
                                                          )
        pipeline = pipe.Pipeline(self, "Pipeline",
                                    pipeline_name="testing-pipeline-cdk",
                                    cross_account_keys=False)
        synth = cdkpipe.ShellStep("Synth",
                                  install_commands=[
                                      'pip install -r requirements.txt'
                                  ],
                                  commands=[
                                      'npx cdk synth'
                                  ],
                                  input=git_input
                                  )
        cdk_pipeline = cdkpipe.CodePipeline(self, "CodePipeline",
                                            synth=synth,
                                            code_pipeline=pipeline,
                                            self_mutation=True
                                            )
        deployment_wave = cdk_pipeline.add_wave("Deployment-wave")
        deployment_wave.add_stage(DeployStage(self, 'DeployStagestuff',
                                              env=Environment(account='061515210591', region='eu-west-1')
                                              ) 
                                )
