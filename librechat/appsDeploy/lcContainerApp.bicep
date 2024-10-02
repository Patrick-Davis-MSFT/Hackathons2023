@description('Container App  Enviroment  Name')
param containerAppEnvName string
//@description('Key Vault Name')
//param keyVaultName string
@description('Specifies the App User Assigned Identity Name')
param appUserAssignedIdentityName string
@description('Specifies the container name')
param containerAppName string = 'meilisearch'
@description('Specifies the docker container image to deploy.')
param containerImage string = 'getmeili/meilisearch:v1.7.3'
// parameters for app 
param targetPort int = 80
param minReplicas int = 1
param maxReplicas int = 3
@description('Number of CPU cores the container can use. Can be with a maximum of two decimals.')
param cpuCore string = '0.5'
@description('Amount of memory (in gibibytes, GiB) allocated to the container up to 4GiB. Can be with a maximum of two decimals. Ratio with CPU cores must be equal to 2.')
param memorySize string = '1'
param secretEnv array
param envValues array
param volumeMounts array
param volumes array


//Get Keyvault Object
//resource keyvault 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
//  name: keyVaultName
//}

//Get Container Environment Object
resource containerAppEnv  'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: containerAppEnvName
}

resource appIdentity  'Microsoft.ManagedIdentity/userAssignedIdentities@2023-07-31-preview' existing = {
  name: appUserAssignedIdentityName
}

resource meilinaApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: resourceGroup().location
  identity: {
    userAssignedIdentities: {
      '${appIdentity.id}': {}
  }
    type: 'UserAssigned'
  }
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      secrets: secretEnv
      ingress: {
        external: true
        targetPort: targetPort
        allowInsecure: false
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
      }
    }
    template: {
      containers: [
        {
          name: containerAppName
          image: containerImage
          resources: {
            cpu: json(cpuCore)
            memory: '${memorySize}Gi'
          }
          env: envValues
          volumeMounts: volumeMounts
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }

      volumes: volumes
    }
  }
}
