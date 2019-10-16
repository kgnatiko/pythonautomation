import boto3
import click

session = boto3.Session(profile_name='python')
s3= session.resource('s3')

@click.group()
def cli():
    "Webotron deloy website to  AWS"
    pass
@cli.command('list-bucket-object')
@click.argument('bucket')
def list_bucket_object(bucket):
    "List Objects in an S3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('list-buckets')
def list_buckets():
    "List all s# buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure S3 bucket"
    s3_bucket = s3.create_bucket(Bucket=bucket)
    policy ="""
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
    policy= policy.strip()
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)
    ws = s3_bucket.Website()
    ws.put(WebsiteConfiguration={'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })
    return

if __name__ == '__main__':
    cli()
