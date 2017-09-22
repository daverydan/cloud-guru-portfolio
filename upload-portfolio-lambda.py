# import modules/dependencies
import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
  # create resource
  s3 = boto3.resource('s3')

  # create buckets
  portfolio_bucket = s3.Bucket('portfolio.dwadev.de')
  build_bucket = s3.Bucket('portfoliobuild.dwadev.de')

  # create a StringIO in memory file 
  portfolio_zip = StringIO.StringIO()
  # download zipfile and store in portfolio_zip
  build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

  # Extract, Upload & set ACL
  with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
      obj = myzip.open(nm)
      portfolio_bucket.upload_fileobj(obj, nm,
        ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
      portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
      
  print "Job done!"

  return 'Hello from Lambda'