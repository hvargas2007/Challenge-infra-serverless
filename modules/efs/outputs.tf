output "file_system_id" {
  value = aws_efs_file_system.main.id
}

output "file_system_arn" {
  value = aws_efs_file_system.main.arn
}

output "access_point_id" {
  value = aws_efs_access_point.lambda.id
}

output "access_point_arn" {
  value = aws_efs_access_point.lambda.arn
}

output "mount_target_ids" {
  value = aws_efs_mount_target.main[*].id
}