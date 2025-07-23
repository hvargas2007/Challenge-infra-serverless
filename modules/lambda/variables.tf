variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "source_path" {
  description = "Path to the Lambda function source code"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for Lambda"
  type        = list(string)
}

variable "security_group_id" {
  description = "Security group ID for Lambda"
  type        = string
}

variable "efs_access_point_arn" {
  description = "ARN of the EFS access point"
  type        = string
}

variable "api_gateway_execution_arn" {
  description = "Execution ARN of the API Gateway"
  type        = string
}

variable "efs_mount_target_ids" {
  description = "List of EFS mount target IDs"
  type        = list(string)
  default     = []
}