output "api_gateway_url" {
  description = "URL of the API Gateway"
  value       = module.api_gateway.api_gateway_url
}

output "api_key_value" {
  description = "API Key value for authentication"
  value       = module.api_gateway.api_key_value
  sensitive   = true
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = module.lambda.function_name
}

output "efs_file_system_id" {
  description = "ID of the EFS file system"
  value       = module.efs.file_system_id
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}