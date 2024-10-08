param location string
param serverName string
param databaseName string = 'pgsqlvector'
param adminUsername string
param keyVaultName string
param subnetId string
param virtualNetworkId string
@secure()
param dbpassword string 

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

resource randomPasswordEncode 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'pgsqlvector-password-encode'
  properties: {
    value: uriComponent(dbpassword)
  }
}

resource randomPassword 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'pgsqlvector-password'
  properties: {
    value: dbpassword
  }
}

resource databaseHost 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'db-host'
  properties: {
    value: postgresqlServer.properties.fullyQualifiedDomainName
  }
}
resource databaseUser 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'db-user'
  properties: {
    value: adminUsername
  }
}

resource vectorDBName 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'db-vector'
  properties: {
    value: databaseName
  }
}

resource postgresqlServerConfig 'Microsoft.DBforPostgreSQL/flexibleServers/configurations@2023-12-01-preview' = {
  name: 'azure.extensions'
  parent: postgresqlServer
  properties: {
    value: 'VECTOR'
    source: 'user-override'
  }
}

resource postgresqlServer 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {
  name: serverName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    createMode: 'Default'
    version:'16'
    administratorLogin: adminUsername
    administratorLoginPassword: dbpassword
    storage: {
      storageSizeGB: 32
      autoGrow: 'Enabled'
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    network: {
      delegatedSubnetResourceId: subnetId
      privateDnsZoneArmResourceId: vnetData_privateDnsZone.id
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
}

resource postgresqlDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-12-01-preview' = {
  parent: postgresqlServer
  name: databaseName
  properties: {}
}


resource vnetData_privateDnsZone 'Microsoft.Network/privateDnsZones@2018-09-01' = {
  name: '${serverName}.private.postgres.database.azure.com'
  location: 'global'
}

resource privateDnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: vnetData_privateDnsZone
  name: '${vnetData_privateDnsZone.name}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: virtualNetworkId
    }
  }
}
/*
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2024-01-01' = {
  name: '${serverName}-pe'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${serverName}-plsc'
        properties: {
          privateLinkServiceId: postgresqlServer.id 
          groupIds: [
            'postgresqlServer'
          ]
        }
      }
    ]
  }
}

resource privateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-11-01' = {
  name: '${serverName}-pdzg'
  parent: privateEndpoint
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'config'
        properties: {
          privateDnsZoneId: vnetData_privateDnsZone.id
        }
      }
    ]
  }
}

*/
