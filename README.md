# UploadDynamoS3

These scripts describe the pipeline or process to upload videos to the AWS platform to later retrieve them in a Web Dictionary. First define the structure of the database (relational or not relational). In our case, we are using a non relational DB, DynamoDB from AWS and S3 to store the videos. Then, we slow down individual videos of signs cut/segmented from sign sentences videos because front ends seems to have trouble with short videos (even less than a second). Here we explain how to create these scripts and run them to execute the upload.

## Step 1: Run scriptGloss.py to Obtain Lemmas

To have only one example for each GLOSS, we group all the examples of each gloss and select randomly a video example. To work with gloss, text and lemmas, we use the SPACY library.

1. To run install SPACY, consider using a conda environment

	pip install -U pip setuptools wheel
	pip install -U spacy
	pip install spacy pandas spellchecker
	python -m spacy download es_dep_news_trf

2. Run the script using the command: `python scriptGloss.py --videoPath videoPath`, where videoPath is the path were segmented videos are located
3. The script extracts the lemma and other relevant information from the video filenames in the specified directory.
4. It exports an intermediate file `lemmaPUCP305.csv` with the original raw gloss, lemma, same lemma flag, path, and sentence video for each gloss.

## Step 2: Run addingSentences.py to add the TextSentences information to the csv file

1. Run the script using `python addingSentences.py`
2. The script will add the TextSentences column to a csv file `lemmaPUCP305-reviewed.csv` and may generate a `error_log.txt` if any gloss has errors at their folder name


## Step 3: Modify Speed of Videos

1. Create a list of files and paths in an CSV (or iterate over a folder structure with os.walk(path))
2. The command to modify videos is ffmpeg, visit the official FFmpeg website: [https://ffmpeg.org/](https://ffmpeg.org/), to download.
3. Run slowDownVideos.py, a script that exports in a sh file with a list of ffmpeg commands for each of the videos in the folders specified in a CSV (once more here instead of the list in the CSV file, we can iterate over a folder structure).
4. Run slowDownVideos.sh

	ffmpeg -i listo_1534 -filter:v "setpts=2.0*PTS" listo_output.mp4

where setpts is the parameter to control the speed, i.e., a value of 2 make it twice slower.

## Step 4: Set AWS Environment to Interact through Platform or Command Line

These steps can either be executed from the AWS platform or by command line through AWS API. We do a combination. To execute from the command line, each user needs an access and secret key. Create access key and secret key. Some info [here](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)	

1. Installthe AWS CLI by referring to the [installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
2. Check if the AWS CLI is installed by running the following command:
   ```shell
   aws --version
   ```
3. Configure the AWS credentials to use the AWS CLI by following the [configuration guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)


## Step 5: Integration with scripts for AWS: upload videos to S3

1. Log in to AWS console, go to S3 Console.
2. Create a bucket. In our case we store individual or isolated signs in the bucket 'isolatedsigns', and the sentences in 'sentencesigns'. If you can not see it, you can create another bucket.
3. Create/update a python file (uploadS3boto3.py) that uses the boto AWS library. The main function is s3_client.upload_file(file_name, bucket,object_name). 
4. Check or set the bucket variable to the name of your S3 buckets in the python script: `bucket = 'test-isolatedsigns'` and `bucketSentence = 'test-sentencesigns'`
5. Run the following command to execute the script: `python uploadS3boto.py`
6. The script will start uploading the videos to the specified S3 bucket. The progress and any errors encountered during the upload process will be displayed in the terminal.
7. Once the script completes, you can check your S3 bucket in the AWS console to verify that the videos have been successfully uploaded.
<!-- 4. Another option: the file to produce with they python script in the previous stage (step 3), should have this format:

	aws s3api put-object --bucket isolatedsigns --body C:\Users\Gissella_BejaranoNic\Documents\PeruvianSignLanguage\Data\testS3\[fileName] --key [lemma]

	Create this script for only 3-5 files, and test it by running the .sh (executable file), you might need to give execution permissions.

	Run: sh uploadS3.sh -->

## Step 6: Integration with scripts for AWS: Create databae DynamoDB

1. Create/update the createItemsDynamo.py to upload batches of maximum 25 items. The main function receives a json file with the different items, this is how DynamoDB create, updates or remove items.
2. Review the code and make sure the following variables are set correctly:
	- path: The path to the directory containing the video files or the CSV file with the video information.
	- dictTemplate: The template dictionary for creating DynamoDB items. Ensure that the keys match the attribute names in your DynamoDB table.
3. If needed, modify the code to extract the relevant information from your video files or CSV file. Update the dictActual dictionary accordingly to include the desired attributes and values (For example adding the Webname)

Note: If you need to update `lemmaPUCP305-reviewed.csv` adding a column make sure it is updated in the dictActual dictionary in the createItemsDynamo.py

4. Run the following command to execute the script: `python createItemsDynamo.py`
5. The script will read the video files or the CSV file, create DynamoDB items based on the provided template, and batch write the items to DynamoDB.
6. Once the script completes, you can verify the created items in your DynamoDB table using the AWS console.
<!-- 2. Another option: Create a Dynamo table: Dynamodb Standard or Dynamobdb Standard IA

	```
	aws dynamodb create-table \
		--table-name MusicCollection \
		--attribute-definitions AttributeName=Artist,AttributeType=S AttributeName=SongTitle,AttributeType=S \
		--key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
		--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
		
		
	aws dynamodb batch-write-item --request-items file://myfile.json

	https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html
	https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.batch_write_item
	https://turbofuture.com/computers/upload-files-aws-s3-and-dynamodb

	``` -->



<!-- 


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
bash: logInfo: command not found -->

