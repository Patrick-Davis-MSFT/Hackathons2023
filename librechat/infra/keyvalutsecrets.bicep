@description('The name of the Key Vault')
param keyVaultName string

@description('ecrets to be created in the Key Vault')
param secretName string
@secure()
param secretValue string

resource keyVault 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

resource keyVaultSecrets 'Microsoft.KeyVault/vaults/secrets@2024-04-01-preview' =  {
  parent: keyVault
  name: secretName
  properties: {
    value: secretValue
  }
}
