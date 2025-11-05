deploy-lambdas:
	@terraform init
	@echo "📦 Empaquetando todas las lambdas..."
	@bash scripts/packages_lambdas.sh
	@echo "🚀 Aplicando Terraform..."
	@terraform plan -var-file=environments/dev/main.tfvars 
