module "vpc" {
  source = "./modules/vpc"

  project_name = var.project_name
  vpc_cidr     = var.vpc_cidr
}

module "efs" {
  source = "./modules/efs"

  project_name      = var.project_name
  subnet_ids        = module.vpc.private_subnet_ids
  security_group_id = module.vpc.efs_security_group_id
}

module "api_gateway" {
  source = "./modules/api_gateway"

  project_name      = var.project_name
  lambda_invoke_arn = module.lambda.invoke_arn
  stage_name        = var.stage_name
}

module "lambda" {
  source = "./modules/lambda"

  project_name              = var.project_name
  function_name             = "${var.project_name}-api"
  source_path               = "${path.module}/lambda_code"
  subnet_ids                = module.vpc.private_subnet_ids
  security_group_id         = module.vpc.lambda_security_group_id
  efs_access_point_arn      = module.efs.access_point_arn
  api_gateway_execution_arn = module.api_gateway.api_gateway_execution_arn
  efs_mount_target_ids      = module.efs.mount_target_ids
}