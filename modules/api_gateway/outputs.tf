data "aws_region" "current" {}

output "api_gateway_url" {
  value = "https://${aws_api_gateway_rest_api.main.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/${aws_api_gateway_stage.main.stage_name}"
}

output "api_gateway_id" {
  value = aws_api_gateway_rest_api.main.id
}

output "api_gateway_execution_arn" {
  value = aws_api_gateway_rest_api.main.execution_arn
}

output "api_key_id" {
  value = aws_api_gateway_api_key.main.id
}

output "api_key_value" {
  value     = aws_api_gateway_api_key.main.value
  sensitive = true
}