# Building and deploying the lambda

From within this directory
```bash
docker run --rm --platform linux/amd64 -v "$PWD":/var/task lambci/lambda:build-python3.8 pip install -r requirements.txt --target ./packages

cd packages
zip -r ../my-deployment-package.zip .
cd ..
zip -g my-deployment-package.zip lambda.py

aws lambda update-function-code --function-name $lambdaName --zip-file fileb://my-deployment-package.zip
```