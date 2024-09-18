@description('Specifies the name of the Key Vault.')
param keyVaultName string

@description('Specifies the location for all resources.')
param location string

@description('Specifies the ID of the virtual network.')
param virtualNetworkId string

@description('Specifies the ID of the private endpoint subnet.')
param privateEndpointSubnetId string

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

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: containerAppLogAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2021-04-01-preview' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Deny'
      virtualNetworkRules: [
        {
          id: privateEndpointSubnetId
        }
      ]
    }
  }
}

resource privateDnsZone 'Microsoft.Network/privateDnsZones@2024-06-01' = {
  name: 'privatelink.vaultcore.azure.net'
  location: 'global'
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: '${keyVaultName}-pe'
  location: location
  properties: {
    subnet: {
      id: privateEndpointSubnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${keyVaultName}-pe-connection'
        properties: {
          privateLinkServiceId: keyVault.id
          groupIds: [
            'vault'
          ]
        }
      }
    ]
  }
}

resource privateDnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: privateDnsZone
  name: '${privateDnsZone.name}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: virtualNetworkId
    }
  }
}

resource pvtEndpointDnsGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-11-01' = {
  parent: privateEndpoint
  name: 'pdz'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'config'
        properties: {
          privateDnsZoneId: privateDnsZone.id
        }
      }
    ]
  }
  dependsOn: [
    privateEndpoint
    privateDnsZone
  ]
}

resource logAnalyticsWorkspaceKey 'Microsoft.KeyVault/vaults/secrets@2021-04-01-preview' = {
  name: '${keyVault.name}/logAnalyticsWorkspaceKey'
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
  identity: {
    type: 'SystemAssigned'
  }
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

resource containerApp 'Microsoft.App/containerApps@2022-03-01' = {
  name: containerAppName
  location: location
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
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
      revisionSuffix: 'firstrevision'
      containers: [
        {
          name: containerAppName
          image: containerImage
          resources: {
            cpu: json(cpuCore)
            memory: '${memorySize}Gi'
          }
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }
    }
  }
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2020-04-01-preview' = {
  name: guid(containerAppEnv.id, 'KeyVaultSecretsUser')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6') // Key Vault Secrets User role
    principalId: containerAppEnv.identity.principalId
    principalType: 'ServicePrincipal'
  }
}



output containerappsDomain string = containerAppEnv.properties.defaultDomain
output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
output containerappsStaticIP string = containerAppEnv.properties.staticIp
