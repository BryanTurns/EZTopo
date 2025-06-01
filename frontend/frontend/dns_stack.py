from aws_cdk import (
    # Duration,
    RemovalPolicy,
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as certificatemanager,
    aws_route53 as route53,
    aws_route53_targets as targets
)
from constructs import Construct

class DNSStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            bucket_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        
        # The code that defines your stack goes here
        bucket = s3.Bucket.from_bucket_name(
            self, "bryanturns.com-bucket",
            bucket_name=bucket_name,
        )
        
        certificate_arn = "arn:aws:acm:us-east-1:985923204824:certificate/ac6cbbc9-7130-4d8a-ba19-2764ed5431c1"
        domain_cert = certificatemanager.Certificate.from_certificate_arn(self, "domainCert", certificate_arn)

        cloudfront_distribution = cloudfront.Distribution(
            self, "bryanturns.com-distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3StaticWebsiteOrigin(bucket), 
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED
            ),
            default_root_object="index.html",
            certificate=domain_cert,
            domain_names=["bryanturns.com"]
        )

        hosted_zone_id = "Z02013281HPCE51F16BDM" 

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "bryanturns.com-hostedzone",
            hosted_zone_id=hosted_zone_id,
            zone_name="bryanturns.com" 
        )

        route53.ARecord(
            self, "bryanturns.com-aliasrecord",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(cloudfront_distribution)),
            zone=hosted_zone
        )
