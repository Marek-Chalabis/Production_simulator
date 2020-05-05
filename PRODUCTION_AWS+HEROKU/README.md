# Instructions for moving the database to aws, and deploy website on heroku  

1 Run this installations

	pip install psycopg2 django-storages boto3
2. Create DB on AWS->RDS(Postgresql):

	*Important Connectivity->Publicly accessible->set "Yes"
	save:
	
	DB instance identifier = "***"
	
	Master username = "***"
	
	Master password = "***"
	
	Endpoint = "***.amazonaws.com"
	
	*save region it could be necessary to add it later in settings
	
	region = Europe (London) "eu-west-2"
2. Create server in PostgreSQL

	Host name/address = Endpoint
	
	Username = Master username
	
	Password = Master password
	
	* IF YOU GOT ERROR-timeout expired or letter have any DB connection problems:
	
		DB->Security Groups->Inbound/Outbound rules edit->Type-PosgreSQL Source anywhere->save
3. Run Create_DB_PostgreSQL

4. Create S3 bucket

	Bucket name = "***"
	
	Region = "***"
	
	Go into bucket Permision->Cors Configuration paste this configuration and save:
	
		<?xml version="1.0" encoding="UTF-8"?>
		<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
		<CORSRule>
    			<AllowedOrigin>*</AllowedOrigin>
    			<AllowedMethod>GET</AllowedMethod>
   			 <AllowedMethod>POST</AllowedMethod>
   			 <AllowedMethod>PUT</AllowedMethod>
    		<AllowedHeader>*</AllowedHeader>
		</CORSRule>
		</CORSConfiguration>
7. Create user for S3 in AWS->IAM(User->Add user)

	check Programmatic access (allows user to make updates etc.)
	
	Next->Attach existing policies directly->check AmazonS3FullAccess
	
	Next....Create:
	
	User = "***"
		
	Access key ID = "***"
		
	Secret access key = "***"
	
8. Establish connection in django, copy this lines:

	AWS_ACCESS_KEY_ID = Access key ID
	AWS_SECRET_ACCESS_KEY = Secret access key
	AWS_STORAGE_BUCKET_NAME = Bucket name
9. Add into INSTALLED_APPS(Django->settings):
	'storages',
	
10. Add into setting:
	(optional)AWS_S3_REGION_NAME = Region for example = "eu-west-2"
	AWS_S3_FILE_OVERWRITE = False 
	AWS_DEFAULT_ACL = None
	DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 
	STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 
	
11. Comment out save method in users->models->Profile

12. Upload css/profile_images files into S3

13. Create Heroku account and start project
	project name = "***"
	
14. Download GIT

15. Set virtual environment for your project

16. Pip install:
	pip install django django-filter django-storages boto3 pillow gunicorn whitenoise
	
17. Set requirements.txt for Heroku, run terminal in yout virtual enviroment and run this commend:
	pip freeze > requirements.txt
	* open requirements.txt and change:
		requests==2.22.0 -> requests==2.23.0
		if there is a lower version
		
18. Create Runtime.txt
	Write there Python version example = python-3.8.1
	
19. Create Procfile WITHOUT ANY EXTANSION	
	Write: 
		web: gunicorn projectname.wsgi --log-file -
		example = web: gunicorn production_simulator.wsgi --log-file -
		
20. Copy url of your created app in Heroku

21. In settings(django), cop this into ALLOWED_HOSTS
	example = ALLOWED_HOSTS = ['productionsimulator.herokuapp.com', '127.0.0.1:8000'] 
	
22. Turn DEBUG to False

23. Go to users->models->Profile-> comment def function
	* create lambda function(AWS)
	
24. In project on Heorku go to Settings->Add Buildpack->choose python

25. Add this in setting:
	STATIC_ROOT = os.path.join(BASE_DIR, 'staticfile')
	
26. Add this to MIDDLEWARE:
	'whitenoise.middleware.WhiteNoiseMiddleware'
	
27. Create a private respository on Github

28. Go to Github and push PRIVATE project

29. Go to Heroku app->Deploy
	Deployment method -> GitHub
	Connect to GitHub -> Find your app -> connect
	Manual deploy -> Deploy branch
	
30. Your app is runinng


