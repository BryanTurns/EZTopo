#!/usr/bin/env python3

import aws_cdk as cdk

from frontend.base_frontend_stack import BaseFrontendStack 
from frontend.eztopo_frontend_stack import EZTopoFrontendStack
from frontend.base_frontend_distribution_stack import BaseFrontendDistributionStack
from frontend.eztopo_distribution_stack import EZTopoDistributionStack

app = cdk.App()
base_frontend_stack = BaseFrontendStack(app, "BaseFrontendStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )
base_frontend_distribution_stack = BaseFrontendDistributionStack(app, "BaseFrontendDistributionStack", base_bucket_name=base_frontend_stack.bucket_name)

eztopo_frontend_stack = EZTopoFrontendStack(app, "EZTopoFrontendStack")
eztopo_distribution_stack = EZTopoDistributionStack(app, "EZTopoFrontendDistributionStack", eztopo_bucket_name=eztopo_frontend_stack.bucket_name)


app.synth()
