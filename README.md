These scripts describe the pipeline or process to upload videos to the AWS platform to later retrieve them in a Web Dictionary. First define the structure of the database (relational or not relational). In our case, we are using a non relational DB, DynamoDB from AWS and S3 to store the videos. Then, we slow down individual videos of signs cut/segmented from sign sentences videos because front ends seems to have trouble with short videos (even less than a second). Here we explain how to create these scripts and run them to execute the upload.

------------------- Modify Speed of videos ------------

1. Create a list of files and paths in an CSV (or iterate over a folder structure with os.walk(path))
2. The command to modify videos is ffmpeg
2. Run slowDownVideos.py, a script that exports in a sh file with a list of ffmpeg commands for each of the videos in the folders specified in a CSV (once more here instead of the list in the CSV file, we can iterate over a folder structure).
3. Run slowDownVideos.sh

	ffmpeg -i listo_1534 -filter:v "setpts=2.0*PTS" listo_output.mp4

where setpts is the parameter to control the speed, i.e., a value of 2 make it twice slower.

----------- Creation of scripts and files to upload ----------------

To have only one example for each GLOSS, we group all the examples of each gloss and select randomly a video example. To work with gloss, text and lemmas, we use the SPACY library.

1. To run install SPACY, consider using a conda environment

	pip install -U pip setuptools wheel
	pip install -U spacy
	python -m spacy download en_core_web_sm
	python -m spacy download es_core_news_sm

2. Update python file scriptGlosas.py with the desired parameters.
2. Fix script to obtain the name of the file of the video before the underscore (_), and the lemma (Spacy library is supposed to work with this but maybe other library can help too). We also fix mispelling with something like a database provided by SPACY, such as 'es_core_news_sm'.

3. Update the script to produce a text file (with extension .sh) that list all the pushes/loads to do to AWS. For example, uploadS3boto3.py


----------- Set AWS Environment to interact through platform or command line  ----------------------
0. These steps can either be executed from the AWS platform or by command line through AWS API. We do a combination. To execute from the command line, each user needs an access and secret key. Create access key and secret key. Some info here https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html

1. For example, to upload objects by installing AWS api (?) that allows to use command line to control services. More info here:
		https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html
		AWS SDK https://docs.aws.amazon.com/cli/latest/reference/s3api/put-object.html
		put-object https://docs.aws.amazon.com/cli/latest/reference/s3api/put-object.html#examples

5. Install AWS CLI. Ref: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
6. Check AWS CLI was installed:

	(base) C:\Users\Gissella_BejaranoNic>aws --version                                                                            
	
	aws-cli/2.7.16 Python/3.9.11 Windows/10 exe/AMD64 prompt/off   

7. Configure credential to be able to use the commands in the command line. Previously, configure aws credentials: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-region


---------- Integration with scripts for AWS: upload videos to S3----------------------

1. Log in to AWS console, go to S3 Console.
2. Create a bucket. In our case we store individual or isolated signs in the bucket 'isolatedsigns', and the sentences in 'sentencesigns'. If you can not see it, you can create another bucket.
3. First option: create/update a python file (uploadS3boto3.py) that uses the boto AWS library. The main function is s3_client.upload_file(file_name, bucket,object_name). 
	
4. Another option: the file to produce with they python script in the previous stage (step 3), should have this format:

	aws s3api put-object --bucket isolatedsigns --body C:\Users\Gissella_BejaranoNic\Documents\PeruvianSignLanguage\Data\testS3\[fileName] --key [lemma]

	Create this script for only 3-5 files, and test it by running the .sh (executable file), you might need to give execution permissions.

	Run: sh uploadS3.sh

---------------- Integration with scripts for AWS: Create databae DynamoDB --------------
1. First option: create/update the createItemsDynamo.py to upload batches of maximum 25 items. The main function receives a json file with the different items, this is how DynamoDB create, updates or remove items.

2. Another option: Create a Dynamo table: Dynamodb Standard or Dynamobdb Standard IA

aws dynamodb create-table \
    --table-name MusicCollection \
    --attribute-definitions AttributeName=Artist,AttributeType=S AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
	
	
aws dynamodb batch-write-item --request-items file://myfile.json

https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_write_item
https://turbofuture.com/computers/upload-files-aws-s3-and-dynamodb








Gabriel useful links

https://aws.amazon.com/amplify/
From Gabriel Paredes - AWS to Everyone 10:15 AM
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.Visualizer.ImportCSV.html
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html
https://aws.amazon.com/es/blogs/aws-spanish/choosing-the-right-dynamodb-partition-key/



Not useful

Create an access point to be able to run the script. It asks for policy/statement

s3://arn:aws:s3:us-east-1:769818850490:accesspoint/accessdiccionario
arn:aws:s3:us-east-1:769818850490:accesspoint/accessdiccionario
accessdiccionario-bttpqeon8hz9jhrtmkut3etz3zysquse1a-s3alias


DOES NOT WORK

	{
	"Sid": "Statement1",
	"Principal": {},
	"Effect": "Allow",
	"Action": [
		"s3:ListJobs",
		"s3:ListMultiRegionAccessPoints"
	],
	"Resource": []
}

SH DOES NOT WORK - I HAD TO INSTALL AWS CLI

bash: logInfo: command not found
curl: Can't open 'C:\Users\Gissella_BejaranoNic\Documents\PeruvianSignLanguage\Data\testS3*'!
curl: try 'curl --help' or 'curl --manual' for more information
curl: (26) Failed to open/read local data from file/application
bash: logInfo: command not found

