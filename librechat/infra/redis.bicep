@description('Specifies the name of the Redis Cache.')
param redisCacheName string

@description('Specifies the location for the Redis Cache.')
param location string

@description('Specifies the pricing tier for the Redis Cache.')
param skuName string = 'Standard'

@description('Specifies the size of the Redis Cache.')
param skuFamily string = 'C'

@description('Specifies the capacity of the Redis Cache.')
param skuCapacity int = 1

@description('Specifies the maximum memory policy for the Redis Cache.')
param maxMemoryPolicy string = 'allkeys-lru'

@description('Subnet for the private end point.')
param subnetId string

@description('Specifies the maximum memory policy for the Redis Cache.')
param virtualNetworkId string

@description('keyvault name to use.')
param keyVaultName string

resource redisCache 'Microsoft.Cache/redis@2024-03-01' = {
  name: redisCacheName
  location: location
  properties: {
    sku: {
      name: skuName
      family: skuFamily
      capacity: skuCapacity
    }
    publicNetworkAccess: 'Disabled'
    enableNonSslPort: false
    redisConfiguration: {
      'maxmemory-policy': maxMemoryPolicy
    }
  }
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: '${redisCacheName}-pe'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${redisCacheName}-plsc'
        properties: {
          privateLinkServiceId: redisCache.id 
          groupIds: [
            'redisCache'
          ]
        }
      }
    ]
  }
}

resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: 'privatelink.redis.cache.windows.net'
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
  name: '${redisCacheName}-pdzg'
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
  name: 'redisPrimaryKey'
  properties: {
    value: listKeys(redisCache.id, '2021-06-01').primaryKey
  }
}

output redisHostName string = redisCache.properties.hostName
//output redisPrimaryKey string = listKeys(redisCache.id, '2021-06-01').primaryKey
