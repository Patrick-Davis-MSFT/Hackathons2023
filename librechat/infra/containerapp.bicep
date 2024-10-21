@description('Specifies the name of the Key Vault.')
param keyVaultName string

@description('Specifies the location for all resources.')
param location string

@description('Specifies the name of the container app environment.')
param containerAppEnvName string
@description('Specifies the ID of the private endpoint subnet.')
param containerAppEnvSubnetId string
@description('Specifies the name of the log analytics workspace.')
param containerAppLogAnalyticsName string
@description('Specifies the name of the log analytics workspace.')
param containerAppInsightssName string

@description('Specifies the name of the container app.')
param containerAppName string

@description('Specifies the docker container image to deploy.')
param containerImage string

@description('Specifies the container port.')
param targetPort int

@description('Number of CPU cores the container can use. Can be with a maximum of two decimals.')
param cpuCore string

@description('Amount of memory (in gibibytes, GiB) allocated to the container up to 4GiB. Can be with a maximum of two decimals. Ratio with CPU cores must be equal to 2.')
param memorySize string

@description('Minimum number of replicas that will be deployed')
param minReplicas int

@description('Maximum number of replicas that will be deployed')
param maxReplicas int

@description('Specifies the name of the storage account.')
param storageAccountName string

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: containerAppLogAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}
resource logAnalyticsWorkspaceKey 'Microsoft.KeyVault/vaults/secrets@2021-04-01-preview' = {
  parent: keyVault
  name: 'loganalyticsworkspacekey'
  properties: {
    value: listKeys(logAnalytics.id, '2020-08-01').primarySharedKey
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: containerAppInsightssName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

resource containerAppEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerAppEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    daprAIInstrumentationKey: appInsights.properties.InstrumentationKey
    vnetConfiguration: {
      infrastructureSubnetId: containerAppEnvSubnetId
      internal: true
    }

  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' existing= {
  name: storageAccountName
}

resource appEnvStorage 'Microsoft.App/managedEnvironments/storages@2024-03-01' = {
  name: 'file'
  parent: containerAppEnv
  properties: {
    azureFile: {
      accessMode: 'ReadWrite'
      accountName: storageAccount.name
      accountKey:  listKeys(storageAccount.id, '2023-05-01').keys[0].value
      shareName: 'file'
    }
  }
}

resource appEnvStorageData 'Microsoft.App/managedEnvironments/storages@2024-03-01' = {
  name: 'data'
  parent: containerAppEnv
  properties: {
    azureFile: {
      accessMode: 'ReadWrite'
      accountName: storageAccount.name
      accountKey:  listKeys(storageAccount.id, '2023-05-01').keys[0].value
      shareName: 'data'
    }
  }
}

resource appEnvStorageMeilina 'Microsoft.App/managedEnvironments/storages@2024-03-01' = {
  name: 'melidata'
  parent: containerAppEnv
  properties: {
    azureFile: {
      accessMode: 'ReadWrite'
      accountName: storageAccount.name
      accountKey:  listKeys(storageAccount.id, '2023-05-01').keys[0].value
      shareName: 'melidata'
    }
  }
}


resource appIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-07-31-preview' = {
  name: 'appIdentity'
  location: location
}

resource appidkvroleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(appIdentity.id, 'KeyVaultSecretsUser')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '4633458b-17de-408a-b874-0445c86b69e6'
    ) // Key Vault Secrets User role
    principalId: appIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
resource appidStorageFileCont 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(appIdentity.id, 'SAFilePrivlagedContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '69566ab7-960f-475b-8e7c-b3118f30c6bd'
    ) // Storage File privlaged Contributor role
    principalId: appIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource appIdAssignmentSMB 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(appIdentity.id, 'SAFileDataSMBShareContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '0c867c2a-1d8c-454a-a3db-ab2ea1bdc8bb'
    ) // Storage File Data SMB Share Contributor role
    principalId: appIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource appIdAssignmentACR 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(appIdentity.id, 'roleAssignmentACR')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '7f951dda-4ed3-4680-a7ca-43fe172d538d'
    ) // AcrPull role
    principalId: appIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: containerAppName
  location: location
  identity: {
    userAssignedIdentities: {
      '${appIdentity.id}': {}
  }
    type: 'UserAssigned'
  }
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      secrets: [
        {
          keyVaultUrl: logAnalyticsWorkspaceKey.properties.secretUri
          name: 'loganalyticsworkspacekey'
          identity: appIdentity.id
        }
      ]
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
          env: [
            {
              name: 'something'
              value: 'somewhere'
            }
            {
              name: 'la-key'
              secretRef: logAnalyticsWorkspaceKey.name
            }
          ]
          volumeMounts: [
            {
              volumeName: 'meilidata'
              mountPath: '/app'
            }
          ]
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }

      volumes: [
        {
          name: 'meilidata'
          storageType: 'AzureFile'
          storageName: 'file'
        }
      ]
    }
  }
}
/*
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(containerAppEnv.id, 'KeyVaultSecretsUser')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '4633458b-17de-408a-b874-0445c86b69e6'
    ) // Key Vault Secrets User role
    principalId: containerAppEnv.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource roleAssignmentSMB 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(containerAppEnv.id, 'SAFileDataSMBShareContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '0c867c2a-1d8c-454a-a3db-ab2ea1bdc8bb'
    ) // Storage File Data SMB Share Contributor role
    principalId: containerAppEnv.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource roleAStorageFileCont 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(containerAppEnv.id, 'SAFilePrivlagedContributor')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '69566ab7-960f-475b-8e7c-b3118f30c6bd'
    ) // Storage File privlaged Contributor role
    principalId: containerAppEnv.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource roleAssignmentACR 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(containerAppEnv.id, 'roleAssignmentACR')
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '7f951dda-4ed3-4680-a7ca-43fe172d538d'
    ) // AcrPull role
    principalId: containerAppEnv.identity.principalId
    principalType: 'ServicePrincipal'
  }
}
  */
output containerappsDomain string = containerAppEnv.properties.defaultDomain
output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
output containerappsStaticIP string = containerAppEnv.properties.staticIp
