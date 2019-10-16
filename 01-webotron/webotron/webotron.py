#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron: Deploy websitstes with AWS.

Webotron automates the process of deploying static websites to AWS.
- Configure aws s3 Buckets
    - Create them
    - Set them up for static website hosting
    - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a content delivery network and SSL with AWS Cloudfront
"""

import boto3
import click
from bucket import BucketManager


session = boto3.Session(profile_name='python')
bucket_manager = BucketManager(session)


@click.group()
def cli():
    """Webotron deloy website to  AWS."""
    pass


@cli.command('list-bucket-object')
@click.argument('bucket')
def list_bucket_object(bucket):
    """List Objects in an S3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('list-buckets')
def list_buckets():
    """List all s# buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)


def upload_files(s3_bucket, path, key):
    """Upload path to s3 bucket at key."""
    content_type = mimetypes.guess_type(key)[0] or 'text/plain'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType': content_type
        })


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync content of PATHNAME to Bucket."""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
