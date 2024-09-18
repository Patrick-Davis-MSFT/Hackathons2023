param cosmosDbAccountName string
param location string
param subnetId string
param keyVaultName string
param virtualNetworkId string
param collectionName string = 'librechat'

resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2021-04-15' = {
  name: cosmosDbAccountName
  location: location
  kind: 'MongoDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    capabilities: [
      {
        name: 'EnableMongo'
      }
    ]
  }
}

resource cosmosDbDatabase 'Microsoft.DocumentDB/databaseAccounts/mongodbDatabases@2021-04-15' = {
  name: 'librechat'
  parent: cosmosDbAccount
  properties: {
    resource: {
      id: 'librechat'
    }
    options: {}
  }
}

resource cosmosDbCollection 'Microsoft.DocumentDB/databaseAccounts/mongodbDatabases/collections@2021-04-15' = {
  name: collectionName
  parent: cosmosDbDatabase
  properties: {
    resource: {
      id: collectionName
    }
    options: {}
  }
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: '${cosmosDbAccountName}-pe'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${cosmosDbAccountName}-plsc'
        properties: {
          privateLinkServiceId: cosmosDbAccount.id
          groupIds: [
            'MongoDB'
          ]
        }
      }
    ]
  }
}

resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.documents.azure.com'
  location: 'global'
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

resource privateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-11-01' = {
  name: '${cosmosDbAccountName}-pdzg'
  parent: privateEndpoint
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
}

resource keyVault 'Microsoft.KeyVault/vaults@2021-04-01-preview' existing = {
  name: keyVaultName
}


resource keyVaultSecret 'Microsoft.KeyVault/vaults/secrets@2021-04-01-preview' = {
  parent: keyVault
  name: 'cosmosDbConnectionString'
  properties: {
    value: 'mongodb://${cosmosDbAccount.properties.documentEndpoint}:${cosmosDbAccount.listKeys().primaryMasterKey}@${cosmosDbAccount.properties.documentEndpoint}:10255/${cosmosDbDatabase.name}?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@${cosmosDbAccountName}@'
  }
}

output connectionStringSecretId string = keyVaultSecret.id
