#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Webotron: Deploy websitstes with AWS.

Webotron automates the process of deploying static websites to AWS.
- Configure aws s3 Buckets
    - Create them
    - Set them up for static website hosting
    - Deploy local files to them
- Configure DNS with AWS Route 53
- Configure a content delivery network and SSL with AWS Cloudfront
"""
from pathlib import Path
import mimetypes
import boto3
import click



session = boto3.Session(profile_name='python')
s3 = session.resource('s3')


@click.group()
def cli():
    """Webotron deloy website to  AWS."""
    pass


@cli.command('list-bucket-object')


@click.argument('bucket')
def list_bucket_object(bucket):
    """List Objects in an S3 bucket."""
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('list-buckets')
def list_buckets():
    """List all s# buckets."""
    for bucket in s3.buckets.all():
        print(bucket)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = s3.create_bucket(Bucket=bucket)
    policy = """
    {
        "Version":"2012-10-17",
        "Statement":[{
        "Sid":"PublicReadGetObject",
        "Effect":"Allow",
        "Principal": "*",
        "Action":["s3:GetObject"],
        "Resource":["arn:aws:s3:::%s/*"
          ]
        }
        ]
    }
    """ % s3_bucket.name
    policy = policy.strip()
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)
    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })


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
    s3_bucket = s3.Bucket(bucket)
    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir():
                handle_directory(p)
            if p.is_file():
                upload_files(s3_bucket, str(p), str(p.relative_to(root)))
    handle_directory(root)


if __name__ == '__main__':
    cli()
