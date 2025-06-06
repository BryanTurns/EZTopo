from aws_cdk import (
    # Duration,
    Stack,
    IgnoreMode,
    aws_s3 as s3,
    RemovalPolicy,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct

class EZTopoFrontendStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
    ) -> None:
        super().__init__(scope, construct_id)
        
        # The code that defines your stack goes here
        bucket = s3.Bucket(
            self, "EZTopo.bryanturns.com-bucket",
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                restrict_public_buckets=False,
            ),
            auto_delete_objects=True,
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            website_index_document="index.html",
        )
        self.bucket_name = bucket.bucket_name

        bucket_deployment = s3deploy.BucketDeployment(
            self, "eztopo.bryanturns.com-deployment",
            destination_bucket=bucket,
            sources=[s3deploy.Source.asset(
                "./frontend/eztopo/build",
                # exclude=["**/videos/**"],
                ignore_mode=IgnoreMode.GIT,
            )],
            memory_limit=512,
        )
