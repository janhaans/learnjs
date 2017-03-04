#!/usr/bin/python

import boto3, os, sys

bucket_name = 'learnjs.janhaans'

def extension_to_mime(extension):
	switcher = {
	'html': 'text/html',
	'js': 'text/javascript',
	'ico': 'image/x-icon',
	'jpg': 'image/jpeg',
	'css': 'text/css',
	'png': 'image/png'
	}
	return switcher.get(extension, "")

s3 = boto3.resource('s3')
s3.create_bucket(
	ACL = 'public-read',
	Bucket = bucket_name
	)

bucket_policy = s3.BucketPolicy(bucket_name)
bucket_policy.put(
	Policy =  '''{
	"Version":"2012-10-17",
	"Statement":[{
		"Sid":"PublicReadForGetBucketObjects",
		"Effect":"Allow",
		"Principal":"*",
		"Action":["s3:GetObject"],
		"Resource":["arn:aws:s3:::learnjs.janhaans/*"]
		}]
	}'''
	)
bucket_policy.load()

path = './public'

for dirpath, dirnames, filenames in os.walk(path):
	for filename in filenames:
		filepath = str(os.path.join(dirpath,filename))
		filename = filepath[9:]
		extension = os.path.splitext(filepath)[1][1:]
		mime = extension_to_mime(extension)
		s3.Object(bucket_name,filename).upload_file(filepath,{'ContentType': mime})


bucket_website = s3.BucketWebsite(bucket_name)
bucket_website.put(
	WebsiteConfiguration = {
		'ErrorDocument': {'Key': 'error.html'},
		'IndexDocument': {'Suffix': 'index.html'}
		}
	)
bucket_website.load()