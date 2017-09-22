# import modules/dependencies
import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
  # create resource
  sns = boto3.resource('sns')
  topic = sns.Topic('arn:aws:sns:us-east-1:294373519810:deployPortfolioTopic')
  
  location = {
      "bucketName": 'portfoliobuild.dwadev.de',
      "objectKey": 'portfoliobuild.zip'
  }
  
  try:  
      job = event.get("CodePipeline.job")
      
      if job:
          for artifact in job["data"]["inputArtifacts"]:
              if artifact["name"] == "MyAppBuild":
                location = artifact["location"]["s3Location"]
                
      print "Building portfolio from " + str(location)
      s3 = boto3.resource('s3')
    
      # create buckets
      portfolio_bucket = s3.Bucket('portfolio.dwadev.de')
      build_bucket = s3.Bucket(location["bucketName"])
    
      # create a StringIO in memory file 
      portfolio_zip = StringIO.StringIO()
      # download zipfile and store in portfolio_zip
      build_bucket.download_fileobj(location["objectKey"], portfolio_zip)
    
      # Extract, Upload & set ACL
      with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
          obj = myzip.open(nm)
          portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
          portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
          
      print "Job done!"
      topic.publish(Subject="Portfolio Deploy Successful", Message="Portfolio deployed Successfully.")
      if job:
          codepipeline = boto3.client('codepipeline')
          codepipeline.put_job_success_result(jobId=job["id"])
  except:
      topic.publish(Subject="Portfolio Deploy FAIL", Message="Portfolio deployment FAILED.")
      raise

  return 'Hello from Lambda'