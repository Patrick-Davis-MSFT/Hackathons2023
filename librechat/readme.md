# Deploy librechat to container apps
1. Install pre-req software to the local deployer 
    1. AKS CLI
        ```powershell
        az aks install-cli
        ```
1. Install pre-req software to the baston host
    1. Chocolatity and Restart
        ```powershell
        Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        ```
        
    2. Azure CLI
        ```powershell
        $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; Remove-Item .\AzureCLI.msi
        ```
        
    3. AKS CLI
        ```powershell
        az aks install-cli
        ```

    4. Helm
        ```powershell
        choco install kubernetes-helm
        ```
    
    5. Kubectl and Kubelogin
        ```powershell
        choco install kubernetes-cli azure-kubelogin
        ```

1. deploy the infrastructure
    1. from the folder in ./librechat/infra run the command `az deployment group create --resource-group [resource-group] --template-file main.bicep --parameters "./parameter.json"`

1. Create a new secret in the keyvault with each of the names. You may have to add your client ip or use the VM that was created. Use this tool to get the values [Librechat tools](https://www.librechat.ai/toolkit/creds_generator)
    * librechat-creds-key
    * librechat-creds-iv
    * librechat-jwt-secret
    * librechat-jwt-refresh-secret
    * librechat-meili-master-key
1. Create a librechat env file as needed. The default env file is included here
1. Load the `./loadEnvtoKV.ps1` in the `librechat/scripts/LibreChat-AppDef` directory. The Key Vault was created in the bicep run above
    * You will need to run this from the baston server or add yourself as a Key Vault Secret Contributor and allow your IP address. 
    * Run the command `./loadEnvtoKV.ps1 -envFilePath "[PathToLibrechatFile]" -keyVaultName "[KeyVaultName]"`
    * This will load all the env file to the key vault. Each secret will be in lowercase prefixed with 'lc-'
    * Rerunning this program after updating the `.env` file will update the secret values. Note: Restart the apps once you update the secret values if already deployed 
1. Update and copy the yaml to the root of the file SMB share in the Azure Storage account
