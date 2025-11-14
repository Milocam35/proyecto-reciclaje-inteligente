deploy-lambdas:
	@terraform init
	@echo "📦 Empaquetando todas las lambdas..."
	@bash scripts/packages_lambdas.sh
	@echo "🚀 Desplegando imagen de docker para clasificacion"
	@bash scripts/push_classifier_image.sh
	@echo "🚀 Aplicando Terraform..."
	@terraform plan -var-file=environments/dev/main.tfvars
