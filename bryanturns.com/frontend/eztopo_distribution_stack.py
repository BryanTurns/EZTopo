from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as certificatemanager,
    aws_route53 as route53,
    aws_route53_targets as targets
)
from constructs import Construct

class EZTopoDistributionStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            *,
            eztopo_bucket_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        
        eztopo_zone_id = "Z02013281HPCE51F16BDM" 
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "EZTopoFrontendHostedZone",
            hosted_zone_id=eztopo_zone_id,
            zone_name="bryanturns.com" 
        )
        
        # Base distribution setup
        eztopo_bucket = s3.Bucket.from_bucket_name(
            self, "EZTopoFrontendBucket",
            bucket_name=eztopo_bucket_name,
        )
        eztopo_certificate_arn = "arn:aws:acm:us-east-1:985923204824:certificate/8d01f4e5-f69f-448e-bb31-64fb0d461462"
        eztopo_domain_cert = certificatemanager.Certificate.from_certificate_arn(self, "base-domaincert", eztopo_certificate_arn)
        eztopo_cloudfront_distribution = cloudfront.Distribution(
            self, "EZTopoFrontendDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3StaticWebsiteOrigin(eztopo_bucket), 
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
            certificate=eztopo_domain_cert,
            domain_names=["eztopo.bryanturns.com"]
            
        )
        route53.ARecord(
            self, "EZTopoFrontendARecord",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(eztopo_cloudfront_distribution)),
            zone=hosted_zone,
            record_name="eztopo"
        )
