# FastAPI

Generate Migration:

```bash
alembic revision --autogenerate -m "name"

```

Run Tests:

```bash
 pytest --cov=app --cov-report=term-missing:skip-covered app/tests
```

Deploy on AWS Lambda:

```bash
sam validate

sam build --use-container --debug

sam package --s3-bucket fast-api-bucket --output-template-file out.yml --region sa-east-1

sam deploy --template-file out.yml --stack-name STACKIS --region sa-east-1 --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM
```

Local Test AWS Lambda Function:

```bash
sam local invoke "FastapiExampleLambda" --event aws-local/event.json --env-vars aws-local/env.json
```

```bash
sam local start-api --env-vars aws-local/env.json --host 0.0.0.0
```
