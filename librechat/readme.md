# Deploy Librechat to Container Apps
> Note All resources are restricted to the network except the Azure Container Registry by default. No RBAC roles or IP allowances are enabled for the user by default.
> Note: No resources are sized for production loads. All resources are sized to minimize costs

1. Download Librechat Repository to the `librechat/scripts` or run `git clone https://github.com/danny-avila/LibreChat.git` in the folder
1. Create a Librechat `.env` and `librechat.yaml` file following the instructions in the Librechat documentation. The Example files are included in the folder `librechat/examples`. See Librechat documentation on file configuration instructions.
1. Optional: Run librechat locally in docker to test your configuration files.
1. Install pre-req software to the local deployment machine. This is needed to fully run the scripts below
    1. Powershell 7.0 or later
    1. AKS CLI
        ```powershell
        az aks install-cli
        ```
    1. Bicep CLI (Requires Azure CLI 2.20.0 or later)
        ```powershell
        az --version
        az bicep version
        az bicep upgrade
        ```
        For bash and linux
        ```bash
        # Fetch the latest Bicep CLI binary
        curl -Lo bicep https://github.com/Azure/bicep/releases/latest/download/bicep-osx-x64
        # Mark it as executable
        chmod +x ./bicep
        # Add Gatekeeper exception (requires admin)
        sudo spctl --add ./bicep
        # Add bicep to your PATH (requires admin)
        sudo mv ./bicep /usr/local/bin/bicep
        # Verify you can now access the 'bicep' command
        bicep --help
        # Done!
        ```
1. No Prerequisite software is needed for the bastion host
1. Create the resource group
1. deploy the infrastructure
    1. from the folder in ./librechat/infra run the command `az deployment group create --resource-group [resource-group] --template-file main.bicep --parameters "./parameter.json"`
1. Check that the test container app, starting with `app-` is the accessible though the bastion box. This verifies network connectivity and DNS resolution to the Container Apps Environment. Note this is not accessible from the local browser.
1. Create a new secret in the keyvault with each of the names. You may have to add your client ip or use the VM that was created. Use this tool to get the values [Librechat tools](https://www.librechat.ai/toolkit/creds_generator)
    * librechat-creds-key
    * librechat-creds-iv
    * librechat-jwt-secret
    * librechat-jwt-refresh-secret
    * librechat-meili-master-key
1. Load the `./loadEnvtoKV.ps1` in the `librechat/scripts/LibreChat-AppDef` directory. The Key Vault was created in the bicep run above
    * You will need to run this from the baston server or add yourself as a Key Vault Secret Contributor and allow your IP address. 
        * Tested with adding the installing users IP address to the allowed addresses on Key Vault and the `Key Vault Administrator` or `Key Vault Contributor` role to the deploying user.
    * Run the command from the `librechat/scripts` folder  `./loadEnvtoKV.ps1 -envFilePath "[PathToLibrechatFile]" -keyVaultName "[KeyVaultName]"`
    * This will load all the env file to the key vault. Each secret will be in lowercase prefixed with 'lc-'
    * Rerunning this program after updating the `.env` file will update the secret values. Note: Restart the apps once you update the secret values if already deployed 
1. Update and copy the librechat.yaml to the root of the file SMB share in the Azure Storage account. Note: The YAML will be accessible in the containers at `/app/librechat.yaml`
1. Build the Librechat container using either local docker and push the image to docker under the name `azurelibrechat` or run the command `az acr build -r [ACR Service Name] -t [ACR LOGIN SERVER]/azurelibrechat -f Dockerfile .` from the LibreChat code directory from step one. Note you may have to delete the `data-node` directory.
    * Follow the Librechat documentation for docker to build and push the container to your ACR. 
1. From the folder `librechat/appsDeploy` run the command `az deployment group create --resource-group [resource-group] --template-file main.bicep --parameters "./parameter.json"` 
    * The parameter file needs to be created by hand or just enter the input manually
    * The following Librechat parameters are automatically configured. These are in addition to the `.env` file parameters
        * For the meilisearch container: MEILI_HOST
        * For the meilisearch container: MEILI_NO_ANALYTICS
        * For the meilisearch container: EMBEDDINGS_PROVIDER
        * For the meilisearch container: RAG_AZURE_OPENAI_API_VERSION
        * For the meilisearch container: EMBEDDINGS_MODEL
        * For the meilisearch container: AZURE_OPENAI_API_KEY
        * For the meilisearch container: AZURE_OPENAI_ENDPOINT
        * For the meilisearch container: RAG_AZURE_OPENAI_ENDPOINT
        * For the meilisearch container: RAG_AZURE_OPENAI_API_KEY
        * For the rag_api container: RAG_PORT
        * For the rag_api container: EMBEDDINGS_PROVIDER
        * For the rag_api container: RAG_AZURE_OPENAI_API_VERSION
        * For the rag_api container: EMBEDDINGS_MODEL
        * For the rag_api container: AZURE_OPENAI_API_KEY
        * For the rag_api container: AZURE_OPENAI_ENDPOINT
        * For the rag_api container: RAG_AZURE_OPENAI_ENDPOINT
        * For the rag_api container: RAG_AZURE_OPENAI_API_KEY
        * For the librechat container: NODE_ENV
        * For the librechat container: MEILI_HOST
        * For the librechat container: RAG_PORT
        * For the librechat container: RAG_API_URL
        * The setting for HOST, PORT are ignored
        * The setting for DOMAIN_CLIENT and DOMAIN_SERVER are dynamically overwritten
1. Librechat will be available on the bastion host at the URL noted in the librechat container app in the resource group.
