# Internal cluster for Azure Government using an NGINX ingress controller
> Tested on 09042024 in US Government Cloud in PowerShell

This document will describe how to create a private AKS cluster with a private NGINX controller

## References
* [AKS Constructor](https://azure.github.io/AKS-Construction/)
* [Configure NGINX ingress controller to support Azure private DNS zone with application routing add-on](https://learn.microsoft.com/en-us/azure/aks/create-nginx-ingress-private-controller)
* [Managed NGINX Ingress with the application routing Add-on](https://learn.microsoft.com/en-us/azure/aks/app-routing)
* [Tutorial: Deploy Azure Bastion by using specified settings](https://learn.microsoft.com/en-us/azure/bastion/tutorial-create-host-portal)
* [Azure Kubelogin](https://azure.github.io/kubelogin/install.html)
* [NGINX Annotations](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/)
* [Azure LoadBalancer Annotations](https://cloud-provider-azure.sigs.k8s.io/topics/loadbalancer/#loadbalancer-annotations)
* [Azure App Gateway Annotations](https://azure.github.io/application-gateway-kubernetes-ingress/annotations/)


## Prerequisites 
Knowledge of Azure, AKS, V-NETS and Bastion hosts 

## Steps
### 1. Create a private aks cluster using the AKS Cluster
```powershell
az cloud set --name AzureUSGovernment
az login
# Create Resource Group
az group create -l CLOUD -n RESOURCE_GROUP
 
# Deploy template with in-line parameters
az deployment group create -g RESOURCE_GROUP `
 --template-uri https://raw.githubusercontent.com/Patrick-Davis-MSFT/Hackathons2023/main/aks-internal/main.json ` 
 --parameters `
    resourceName=az-k8s-bd2g `
    upgradeChannel=stable `
    AksPaidSkuForSLA=true `
    SystemPoolType=Standard `
    agentVMSize=Standard_D2ds_v5 `
    agentCountMax=20 `
    osDiskType=Managed `
    osDiskSizeGB=32 `
    custom_vnet=true `
    vnetAksSubnetAddressPrefix=10.240.0.0/24 `
    CreateNetworkSecurityGroups=true `
    enable_aad=true `
    AksDisableLocalAccounts=true `
    enableAzureRBAC=true `
    adminPrincipalId=$(az ad signed-in-user show --query id --out tsv) `
    privateLinks=true `
    enableTelemetry=false `
    networkPolicy=azure `
    networkPluginMode=Overlay `
    podCidr=10.244.0.0/16 `
    enablePrivateCluster=true `
    diskCSIDriver=false `
    aksOutboundTrafficType=natGateway `
    createNatGateway=true

 
```

>Note: The main.json from the construction helper has been altered to limit the deployed availability zones due to capacity restrictions in this test. 

This will create the private AKS cluster and associated VNETS. 

### 2. Create a Bastion and a VM inside the same VNET following the standard methodology
From this point onward all commands are run on the baston host

### 3. Install required programs on the bastion host

1. Azure CLI
    ```powershell
    $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; Remove-Item .\AzureCLI.msi
    ```
    
1. AKS CLI
   ```powershell
   az aks install-cli
   ```
   
1. Chocolatity (If the previous does not install kubectl)
    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```
    
1. Kubectl and Kubelogin
    ```powershell
    choco install kubernetes-cli azure-kubelogin
    ```

### 4. Login to AKS
Get the commands from the connect portion on the portal
```powershell
az cloud set --name AzureUSGovernment
az login

az account set --subscription SUBSCRIPTION_ID
az aks get-credentials --resource-group RESOURCE_GROUP --name AKS_NAME

#test that you can communicate with AKS
kubectl get nodes

```

Test the connection with `kubectl get nodes`

### 5. Enable the routing add-on
```powershell
az aks approuting enable --resource-group RESOURCE_GROUP --name AKS_NAME
```
### 6. Create a private dns and link it to the AKS VNET

use either the below PowerShell or the Portal

```powershell
az network private-dns zone create --resource-group RESOURCE_GROUP --name something.com

az network private-dns link vnet create --resource-group RESOURCE_GROUP `
  --name myDNSLink `
  --zone-name something.com `
  --virtual-network AKS_VNET_NAME `
  --registration-enabled false
``` 
> If the bastion is in a peered vnet add the private dns link to the peered vnet as well

### 7. Register the DNS with AKS 
```powershell
$ZONEID=$(az network private-dns zone show --resource-group RESOURCE_GROUP --name something.com --query "id" --output tsv)

az aks approuting zone add --resource-group RESOURCE_GROUP --name AKS_SERVICE --ids=$ZONEID --attach-zones

```

### 8. Run an altered version of the ingress controller daemon on the in power shell


```powershell
az aks command invoke -g RESOURCE_GROUP -n AKS_SERVICE --command " curl -v -sL https://raw.githubusercontent.com/Patrick-Davis-MSFT/Hackathons2023/main/aks-internal/ingressPost.sh | bash -s -- -r https://github.com/Azure/AKS-Construction/releases/download/0.10.7 -p ingress=nginx -p ingressEveryNode=true 2>&1 | tee /tmp/deploy.log "
```

> Note This is a custom script changed for internal routing if you ran the invoke command in the above script from from the construction helper the previous nginx helm install must be removed before running this command. Run `helm list -A` to find the install and then `helm uninstall nginx-ingress -n ingress-basic` and `kubectl delete NginxIngressController nginx-internal` to remove it

### 9. Deploy sample applications 

```powershell
kubectl create namespace hello-web-app-routing
kubectl -n hello-web-app-routing apply -f https://raw.githubusercontent.com/Patrick-Davis-MSFT/Hackathons2023/main/aks-internal/deployment.yaml
kubectl -n hello-web-app-routing apply -f https://raw.githubusercontent.com/Patrick-Davis-MSFT/Hackathons2023/main/aks-internal/service.yaml
kubectl -n hello-web-app-routing apply -f https://raw.githubusercontent.com/Patrick-Davis-MSFT/Hackathons2023/main/aks-internal/ingress.yaml

#verify services are created in AKS 
kubectl -n hello-web-app-routing get deployments
kubectl -n hello-web-app-routing get pods 
kubectl -n hello-web-app-routing get service
kubectl -n hello-web-app-routing get ingress
```
> Note it will take a few minutes to assign an IP address in the ingress controller. 

### 10. Verify that the DNS now has a record for hello.something.com pointing to the private ip of the aks loadbalancer in the MC_* resource group

`az network private-dns record-set a list --resource-group RESOURCE_GROUP --zone-name something.com`
View the site at the url
* `curl http://hello.something.com`
* [Website](http://hello.something.com) at http://hello.something.com on the Bastion host
