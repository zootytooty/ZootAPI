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

# Push to AWS
aws lambda update-function-code --publish --function-name Get-Gigs --zip-file fileb://ZootAPI.zip