#!/usr/bin/python
#Checking avaialable S3 buckets
#We should have aws and awscli installed

import boto3
from pprint import pprint
from subprocess import Popen, PIPE

clnt = boto3.client('s3')
response = clnt.list_buckets()
print "%30s %15s %21s %18s %11s %13s"%("BucketName", "Region", "Versioning", "S3Logging", "TotalSize", "TotalObjects")
for i in response["Buckets"]:
        try:
                print "%30s"%(i["Name"]),
                resourceLocation = clnt.get_bucket_location(
                Bucket=i["Name"])
                if resourceLocation['LocationConstraint']:
                        print "%15s"%(resourceLocation['LocationConstraint']),
                else:
                        print "%15s"%("us-east-1"),
                resourceVersioning = clnt.get_bucket_versioning(Bucket=i["Name"])
                if resourceVersioning.get('Status', None):
                    print "%21s"%("Versioning"+str(resourceVersioning['Status'])),
                else:
                    print "%21s"%("VersioningNotEnabled"),
                resourceBucktLogging = clnt.get_bucket_logging(Bucket=i["Name"])
                if resourceBucktLogging.get('LoggingEnabled', None):
                    print "%18s"%("LoggingEnabled"),
                else:
                    print "%18s"%("LoggingNotEnabled"),
                
                p = Popen("aws s3 ls s3://"+str(i["Name"])+" --recursive --human-readable --summarize", shell=True, stdout=PIPE)
                (pOut, pErr) = p.communicate()
                if pErr:
                    print "Unable to get bucket size", pErr
                else:
                    print "%11s %13s"%(pOut.strip().split('\n')[-1].strip().split(":")[1], pOut.strip().split('\n')[-2].strip().split(":")[1])
        except Exception as ex:
                print ex