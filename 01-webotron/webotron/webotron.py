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

if __name__ == '__main__':
    cli()
