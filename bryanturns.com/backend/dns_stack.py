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
            base_bucket_name: str,
            eztopo_bucket_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        
        # Configure DNS records
        hosted_zone_id = "Z02013281HPCE51F16BDM" 
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self, "bryanturns.com-hostedzone",
            hosted_zone_id=hosted_zone_id,
            zone_name="bryanturns.com" 
        )
        
        # Base distribution setup
        base_bucket = s3.Bucket.from_bucket_name(
            self, "bryanturns.com-bucket",
            bucket_name=base_bucket_name,
        )
        base_certificate_arn = "arn:aws:acm:us-east-1:985923204824:certificate/ac6cbbc9-7130-4d8a-ba19-2764ed5431c1"
        base_domain_cert = certificatemanager.Certificate.from_certificate_arn(self, "base-domaincert", base_certificate_arn)
        base_cloudfront_distribution = cloudfront.Distribution(
            self, "bryanturns.com-distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3StaticWebsiteOrigin(base_bucket), 
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
            certificate=base_domain_cert,
            domain_names=["bryanturns.com"]
        )
        route53.ARecord(
            self, "bryanturns.com-aliasrecord",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(base_cloudfront_distribution)),
            zone=hosted_zone
        )
        
        # EZTopo distribution setup
        eztopo_bucket = s3.Bucket.from_bucket_name(
            self, "eztopo-bucket",
            bucket_name=eztopo_bucket_name,
        )
        eztopo_certificate_arn = "arn:aws:acm:us-east-1:985923204824:certificate/8d01f4e5-f69f-448e-bb31-64fb0d461462"
        eztopo_domain_cert = certificatemanager.Certificate.from_certificate_arn(self, "eztopo-domaincert", eztopo_certificate_arn)
        eztopo_cloudfront_distribution = cloudfront.Distribution(
            self, "eztopo-distribution",
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
            self, "eztopo-aliasrecord",
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(base_cloudfront_distribution)),
            zone=hosted_zone,
            record_name="eztopo",
        )
