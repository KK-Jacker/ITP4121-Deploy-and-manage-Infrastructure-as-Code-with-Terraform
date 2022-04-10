cdktf deploy --auto-approve
terraform output -state=terraform.iShare_stack.tfstate -json > stack_output.json