----------- creation of scripts and files to upload ----------------

1. Update python file scriptGlosas.py. To run install SPACY, consider using a conda environment

	pip install -U pip setuptools wheel
	pip install -U spacy
	python -m spacy download en_core_web_sm
	python -m spacy download es_core_news_sm

2. Fix script to obtain the name of the file of the video before the underscore (_), and the lemma (Spacy library is supposed to work with this but maybe other library can help us too).

3. Update the script to produce a text file (with extension .sh) that list all the pushes/loads to do to AWS


----------- integration with scripts for AWS ----------------------

1. Log in to AWS console, go to S3 Console
2. I have already create a bucket called isolatedSigns, if you can not see it, you can create another bucket.
3. Create access key and secret key. Some info here https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html
4. Upload objects by installing AWS api (?) that allows to use command line to control services. More info here:
		https://docs.aws.amazon.com/AmazonS3/latest/userguide/upload-objects.html
		AWS SDK https://docs.aws.amazon.com/cli/latest/reference/s3api/put-object.html
		put-object https://docs.aws.amazon.com/cli/latest/reference/s3api/put-object.html#examples

5. Install AWS CLI. Ref: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
6. Check AWS CLI was installed:

	(base) C:\Users\Gissella_BejaranoNic>aws --version                                                                            
	aws-cli/2.7.16 Python/3.9.11 Windows/10 exe/AMD64 prompt/off   

7. Configure credential to be able to use the commands in the command line. Previously, configure aws credentials: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-region

8. The file to produce with they python script in the previous stage (step 3), should have this format:

	aws s3api put-object --bucket isolatedsigns --body C:\Users\Gissella_BejaranoNic\Documents\PeruvianSignLanguage\Data\testS3\[fileName] --key [lemma]

9. Create this script for only 3-5 files, and test it by running the .sh (executable file), you might need to give execution permissions.

10. Run: sh uploadS3.sh

---------------- S3 and upload to DynamoDB --------------

1. Create a Dynamo table: Dynamodb Standard or Dynamobdb Standard IA

aws dynamodb create-table \
    --table-name MusicCollection \
    --attribute-definitions AttributeName=Artist,AttributeType=S AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
	
	
aws dynamodb batch-write-item --request-items file://myfile.json

https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_write_item

https://turbofuture.com/computers/upload-files-aws-s3-and-dynamodb


------------------- Modify Speed of videos ------------

1. Create a list of files and paths in an CSV
2. Run slowDownVideos.py, a script that exports in a sh a list of ffmpeg commands for each of the folders in CSV
3. Run slowDownVideos.sh

setpts= 2 make it twice slower

ffmpeg -i listo_1534 -filter:v "setpts=2.0*PTS" listo_output.mp4





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

