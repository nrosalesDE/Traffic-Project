$ErrorActionPreference = "Stop"

$AWS_REGION = "us-east-2"
$AWS_ACCOUNT_ID = "359655298703"
$ECR_REPO_NAME = "traffic-transform-lambda"
$LAMBDA_FUNCTION_NAME = "Tranform_Lambda"

$IMAGE_URI = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME`:latest"

Write-Host "Building and pushing Docker image..."
docker buildx build `
  --platform linux/amd64 `
  --provenance=false `
  --sbom=false `
  -t $IMAGE_URI `
  --push .

Write-Host "Updating Lambda function..."
aws lambda update-function-code `
  --function-name $LAMBDA_FUNCTION_NAME `
  --image-uri $IMAGE_URI `
  --region $AWS_REGION

Write-Host "Deployment complete."
Write-Host "Lambda function updated with image:"
Write-Host $IMAGE_URI