
@description('Specifies the location for all resources.')
param location string
@description('Specifies the name of the container app environment.')
param containerAppEnvName string
@description('Specifies the name of the container app default Domain.')
param containerAppDefaultDomain string
@description('Specifies the ID of the virtual network.')
param virtualNetworkId string
@description('Specifies the ID of the private endpoint subnet.')
param privateEndpointSubnetId string
@description('Container Apps Enviroment static IP.')
param containerAppEnvStaticIP string


resource containerAppEnv 'Microsoft.App/managedEnvironments@2022-03-01' existing = {
  name: containerAppEnvName
}

resource privateDnsZoneCA 'Microsoft.Network/privateDnsZones@2024-06-01' = {
  name: containerAppDefaultDomain
  location: 'global'
  dependsOn: [
    containerAppEnv
  ]
}

resource aRecordSet 'Microsoft.Network/privateDnsZones/A@2020-06-01' = {
  parent: privateDnsZoneCA
  name: '*'
  properties: {
    ttl: 3600
    aRecords: [
      {
        ipv4Address: containerAppEnvStaticIP
      }
    ]
  }
}


resource privateDnsZoneLinkCA 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: privateDnsZoneCA
  name: '${privateDnsZoneCA.name}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: virtualNetworkId
    }
  }
}
