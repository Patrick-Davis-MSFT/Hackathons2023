@description('Specifies the name of the container app.')
param containerAppName string = 'app-${uniqueString(resourceGroup().id)}'
@description('Specifies the name of the container app environment.')
param containerAppEnvName string = 'env-${uniqueString(resourceGroup().id)}'
@description('Specifies the name of the log analytics workspace.')
param containerAppLogAnalyticsName string = 'log-${uniqueString(resourceGroup().id)}'
@description('Specifies the name of the log analytics workspace.')
param containerAppInsightsName string = 'ai-${uniqueString(resourceGroup().id)}'
@description('Specifies the name of the virtual network.')
param virtualNetworkName string = 'vnet-${uniqueString(resourceGroup().id)}'
@description('Address prefix')
param vnetAddressPrefix string = '10.0.0.0/16'
@description('Container App environment subnet name')
param containerAppEnvSubnetName string = 'Subnet1'
@description('Container App environment subnet prefix')
param containerAppEnvSubnetPrefix string = '10.0.0.0/21'
@description('Specifies the location for all resources.')
param location string = resourceGroup().location
@description('Specifies the docker container image to deploy.')
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
@description('Specifies the container port.')
param targetPort int = 80
@description('Number of CPU cores the container can use. Can be with a maximum of two decimals.')
@allowed([
  '0.25'
  '0.5'
  '0.75'
  '1'
  '1.25'
  '1.5'
  '1.75'
  '2'
])
param cpuCore string = '0.5'

@description('Amount of memory (in gibibytes, GiB) allocated to the container up to 4GiB. Can be with a maximum of two decimals. Ratio with CPU cores must be equal to 2.')
@allowed([
  '0.5'
  '1'
  '1.5'
  '2'
  '3'
  '3.5'
  '4'
])
param memorySize string = '1'
@description('Minimum number of replicas that will be deployed')
@minValue(0)
@maxValue(25)
param minReplicas int = 1
@description('Maximum number of replicas that will be deployed')
@minValue(0)
@maxValue(25)
param maxReplicas int = 3
@description('Specifies the name of the Key Vault.')
param keyVaultName string = 'kv-${uniqueString(resourceGroup().id)}'
//@description('Specifies the name of the Redis.')
//param redisName string = 'red-${uniqueString(resourceGroup().id)}'
@description('Specifies the name of the private endpoint subnet.')
param privateEndpointSubnetName string = 'Subnet2'
@description('Specifies the private endpoint subnet prefix.')
param privateEndpointSubnetPrefix string = '10.0.8.0/24'
@description('Specifies the name of the Bastion subnet.')
param bastionSubnetName string = 'AzureBastionSubnet'
@description('Specifies the Bastion subnet prefix.')
param bastionSubnetPrefix string = '10.0.9.0/24'
@description('Specifies the name of the Bastion host.')
param bastionHostName string = 'bastion-${uniqueString(resourceGroup().id)}'
@description('Specifies the name of the Windows VM.')
param vmName string = 'vm-${uniqueString(resourceGroup().id)}'
@description('Specifies the admin username for the Windows VM.')
param adminUsername string
@description('Specifies the admin password for the Windows VM.')
@secure()
param adminPassword string
@description('Specifies the size of the Windows VM.')
param vmSize string = 'Standard_DS1_v2'
@description('Specifies the name of the Postgres server.')
param postgreServerName string = 'psql-${uniqueString(resourceGroup().id)}'
@description('Postgree Database Password')
@secure()
param dbpassword string



resource vnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: virtualNetworkName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        vnetAddressPrefix
      ]
    }
    subnets: [
      {
        name: containerAppEnvSubnetName
        properties: {
          addressPrefix: containerAppEnvSubnetPrefix
        }
      }
      {
        name: privateEndpointSubnetName
        properties: {
          addressPrefix: privateEndpointSubnetPrefix
          serviceEndpoints: [
            {
              service: 'Microsoft.KeyVault'
            }
          ]
        }
      }
      {
        name: bastionSubnetName
        properties: {
          addressPrefix: bastionSubnetPrefix
        }
      }
      {
        name: 'vmSubnet'
        properties: {
          addressPrefix: '10.0.10.0/24'
        }
      }
      {
        name: 'vmMongoSubnet'
        properties: {
          addressPrefix: '10.0.11.0/24'
        }
      }
      {
        name: 'vmRedisSubnet'
        properties: {
          addressPrefix: '10.0.12.0/24'
        }
      }
      {
        name: 'storageSubnet'
        properties: {
          addressPrefix: '10.0.13.0/24'
        }
      }
      {
        name: 'acrSubnet'
        properties: {
          addressPrefix: '10.0.14.0/24'
        }
      }
      {
        name: 'postgresSubnet'
        properties: {
          addressPrefix: '10.0.15.0/24'
          delegations: [{
            name: 'Microsoft.DBforPostgreSQL/flexibleServers'
            properties: {
              serviceName: 'Microsoft.DBforPostgreSQL/flexibleServers'
            }
          }]
        }
      }
    ]
  }
}

module keyVaultModule 'keyvault.bicep' = {
  name: 'keyVaultModule'
  params: {
    location: location
    keyVaultName: keyVaultName
    privateEndpointSubnetId: vnet.properties.subnets[1].id
    virtualNetworkId: vnet.id
  }
}

module postgresqlDatabase 'postgresql.bicep' = {
  name: 'postgresqlDatabase'
  params: {
    location: location
    serverName: postgreServerName
    adminUsername: adminUsername
    keyVaultName: keyVaultName
    subnetId: vnet.properties.subnets[8].id
    virtualNetworkId: vnet.id
    dbpassword:dbpassword 
  }
  dependsOn: [ keyVaultModule ]
}

module acrWithPE 'containerreg.bicep' = {
  name: 'acrWithPE'
  params: {
    location: location
    registryName: 'acr${uniqueString(resourceGroup().id)}'
    vnetId: vnet.id
    subnetId: vnet.properties.subnets[7].id
  }
}

module storageAccountMod 'storage.bicep' = {
  name: 'storageAccountMod'
  params: {
    location: location
    storageAccountName: 'sa${uniqueString(resourceGroup().id)}'
    blobContainerName: 'blob'
    smbShareNameConfig: 'file'
    smbShareNameData: 'data'
    subnetId: vnet.properties.subnets[6].id
    keyVaultName: keyVaultName
    virtualNetworkId: vnet.id
  }
  dependsOn: [ keyVaultModule ]
}

module containerAppModule 'containerapp.bicep' = {
  name: 'containerAppModule'
  params: {
    keyVaultName: keyVaultName
    location: location
    containerAppEnvName: containerAppEnvName
    containerAppEnvSubnetId: vnet.properties.subnets[0].id
    containerAppLogAnalyticsName: containerAppLogAnalyticsName
    containerAppInsightssName: containerAppInsightsName
    containerAppName: containerAppName
    containerImage: containerImage
    targetPort: targetPort
    cpuCore: cpuCore
    memorySize: memorySize
    minReplicas: minReplicas
    maxReplicas: maxReplicas
    storageAccountName: storageAccountMod.outputs.storageAccountName
  }
  dependsOn: [ storageAccountMod,keyVaultModule ]
}

module bastionModule 'bastion.bicep' = {
  name: 'bastionModule'
  params: {
    keyVaultName: keyVaultName
    bastionHostName: bastionHostName
    location: location
    bastionSubnetId: vnet.properties.subnets[2].id
    vmName: vmName
    adminUsername: adminUsername
    adminPassword: adminPassword
    vmSize: vmSize
    vmSubnetId: vnet.properties.subnets[3].id
  }
  dependsOn: [
    containerAppModule
    keyVaultModule
  ]
}

module containerAppPE 'ca-privateendpoint.bicep' = {
  name: 'containerAppPE'
  params: {
    containerAppEnvName: containerAppEnvName
    virtualNetworkId: vnet.id
    containerAppDefaultDomain: containerAppModule.outputs.containerappsDomain
    containerAppEnvStaticIP: containerAppModule.outputs.containerappsStaticIP
  }
  dependsOn: [
    containerAppModule
  ]
}

module mongodbModule 'mongodb.bicep' = {
  name: 'mongodbModule'
  params: {
    location: location
    cosmosDbAccountName: containerAppName
    subnetId: vnet.properties.subnets[4].id
    keyVaultName: keyVaultName
    virtualNetworkId: vnet.id
  }
  
  dependsOn: [ keyVaultModule ]
}

/*
module redisModule 'redis.bicep' = {
  name: 'redis-9944'
  params: {
    location: location
    redisCacheName: redisName
    subnetId: vnet.properties.subnets[5].id
    keyVaultName: keyVaultName
    virtualNetworkId: vnet.id
  }
  dependsOn: [ keyVaultModule ]
}
module kvSecrets 'keyvalutsecrets.bicep' = [for secret in libreChatEnvValues: {
  name: 'kvSecrets-${secret.name}'
  params: {
    keyVaultName: keyVaultName
    secretName: secret.name
    secretValue: secret.value
  }
}]
  */

output containerAppFQDN string = containerAppModule.outputs.containerAppFQDN
output containerAppIP string = containerAppModule.outputs.containerappsStaticIP
output containerAppEnvName string = containerAppEnvName
output keyVaultName string = keyVaultName
