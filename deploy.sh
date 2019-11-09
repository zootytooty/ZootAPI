#!/bin/bash

MANIFEST="deploy_manifest"
DEPLOY_PACKAGE="ZootAPI.zip"

if [ -f ./${MANIFEST} ]
then 
    source ${MANIFEST}
else
    echo "Unable to find ./${MANIFEST}"
    exit 1
fi

# Clean up from past releases
if [ -d "package" ]; then rm -Rf package; fi
if [ -f "${DEPLOY_PACKAGE}" ]; then rm -Rf ${DEPLOY_PACKAGE}; fi

# Create directory to house the libraries and install requirements
mkdir ./package
pushd ./package &>/dev/null
pip install -r ../requirements.txt --target .
popd &>/dev/null

# Create working directory
mkdir ./tmp

# Check each item in the manifest exists, if not error out
NUM_DIR=${#DIR[@]}
for ((i=0; i<$NUM_DIR; i++))
do
    if [ ! -d "${DIR[i]}" ]
    then
        echo "Unable to find required directory ${DIR[i]}"
        rm -r ./tmp && exit 1
    else
        cp -r ./${DIR[i]} ./tmp
    fi
done

NUM_FILE=${#FILE[@]}
for ((i=0; i<$NUM_FILE; i++))
do
    if [ ! -f "${FILE[i]}" ]
    then
        echo "Unable to find required file ${FILE[i]}"
        rm -r ./tmp && exit 1
    else
        cp ./${FILE[i]} ./tmp
    fi
done

# Package it up
pushd ./tmp &>/dev/null
zip -r9 ../${DEPLOY_PACKAGE} .
popd &>/dev/null

if [ ! -f "./${DEPLOY_PACKAGE}" ]
then
    echo "Unable to create package for deployment."
    rm -r ./tmp && exit 1
fi

# Push to AWS
aws lambda update-function-code --publish --function-name Get-Gigs --zip-file fileb://ZootAPI.zip