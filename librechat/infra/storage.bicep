@description('Specifies the name of the storage account.')
param storageAccountName string

@description('Specifies the location for the storage account.')
param location string

@description('Specifies the name of the SMB share for configuration.')
param smbShareNameConfig string
@description('Specifies the name of the SMB share for datafiles.')
param smbShareNameData string

@description('Specifies the name of the blob container.')
param blobContainerName string

@description('Specifies the ID of the subnet for the private endpoint.')
param subnetId string

@description('Specifies the ID of the virtual network.')
param virtualNetworkId string

@description('Specifies the name of the Key Vault.')
param keyVaultName string

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
//    allowSharedKeyAccess: false // not recommended for security but Entra RBAC is not supported for container apps storage
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
  }
}

resource fileShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-05-01' = {
  name: '${storageAccount.name}/default/${smbShareNameConfig}'
  properties: {
    shareQuota: 5 // Quota in GB
  }
}

resource fileShareData 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-05-01' = {
  name: '${storageAccount.name}/default/${smbShareNameData}'
  properties: {
    shareQuota: 500 // Quota in GB
  }
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-09-01' = {
  name: '${storageAccount.name}/default/${blobContainerName}'
  properties: {}
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: '${storageAccountName}-pe'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${storageAccountName}-plsc'
        properties: {
          privateLinkServiceId: storageAccount.id
          groupIds: [
            'file'
          ]
        }
      }
    ]
  }
}

resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.blob.core.windows.net'
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
  name: '${storageAccountName}-pdzg'
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
  name: 'storageAccountKey'
  properties: {
    value: listKeys(storageAccount.id, '2021-09-01').keys[0].value
  }
}

output storageAccountName string = storageAccount.name
output smbShareName string = fileShare.name
