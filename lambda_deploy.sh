# *Assumes starting in root*

# Clean up from past releases
if [ -d "package" ]; then rm -Rf package; fi
if [ -f "ZootAPI.zip" ]; then rm -Rf ZootAPI.zip; fi

# Create directory to house the libraries
mkdir package
cd package

# Install requirements & create zip
pip install -r ../requirements.txt --target .
zip -r9 ../ZootAPI.zip .

# Add lambda function & custom dependencies 
cd ../
zip -g ZootAPI.zip zootapi.py gigmanagement.py conf.yaml

zip -g ZootAPI.zip src/zootapi.py src/gigmanagement.py

# Push to AWS
aws lambda update-function-code --publish --function-name Get-Gigs --zip-file fileb://ZootAPI.zip --environment "Variables={RDS_MASTER_USER=RDS_MASTER_USER,RDS_MASTER_PASSWORD=RDS_MASTER_PASSWORD,RDS_DATABASE_NAME=RDS_DATABASE_NAME,RDS_ENDPOINT=RDS_ENDPOINT}"
aws lambda update-function-configuration --function-name Get-Gigs --environment "Variables={RDS_MASTER_USER=RDS_MASTER_USER,RDS_MASTER_PASSWORD=RDS_MASTER_PASSWORD,RDS_DATABASE_NAME=RDS_DATABASE_NAME,RDS_ENDPOINT=RDS_ENDPOINT}"
                                                                                                                


aws lambda update-function-configuration --function-name lambda-func-name --environment '{"Variables":{"FOO":"bar", "BAZ":"blah"}}'