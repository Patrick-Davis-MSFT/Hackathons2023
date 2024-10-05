@description('Container App  Enviroment  Name')
param containerAppEnvName string
@description('Key Vault Name')
param keyVaultName string
@description('Specifies the App User Assigned Identity Name')
param appUserAssignedIdentityName string
@description('Specifies the Azure container registry service name')
param acrService string
@description('Min Replicas for the containers')
param minReplicas int = 1
@description('Max Replicas for the containers')
param maxReplicas int = 3
@description('Number of CPU cores the container can use. Can be with a maximum of two decimals.')
param cpuCore string = '0.5'
@description('Amount of memory (in gibibytes, GiB) allocated to the container up to 4GiB. Can be with a maximum of two decimals. Ratio with CPU cores must be equal to 2.')
param memorySize string = '1'

@description('openai api key for Azure')
@secure()
param azureOpenaiApiKey string
@description('RAG openai api key for Azure')
@secure()
param ragAzureOpenAIKey string
@description('Openai api Base URL for Azure')
param azureOpenaiBaseUrl string
@description('RAG Openai api Base URL for Azure')
param ragAzureOpenaiBaseUrl string
@description('RAG Azure API Version')
param ragAzureAPIVersion string = '2024-06-01'
@description('RAG Azure Deployment Name for Embeddings')
param embeddingsDeployment string

//meilinasearch settings
param meilinaAppName string = 'meilisearch'
param meilinaContainerImage string = 'getmeili/meilisearch:v1.7.3'
param meilinaTargetPort int = 7700

//rag_api settings
param ragApiName string = 'rag-api'
param ragApiContainerImage string = 'ghcr.io/danny-avila/librechat-rag-api-dev-lite:latest'
param ragApiTargetPort int = 8000
param databasePort string = '5432'

//Librechat settings
param lcTargetPort int = 3080
param libreChatContainerService string = 'librechat'
param libreChatImage string = 'azurelibrechat'
param libreChatTag string = 'latest'

//Get Keyvault Object
resource keyvault 'Microsoft.KeyVault/vaults@2024-04-01-preview' existing = {
  name: keyVaultName
}

//Get Container Environment Object
resource containerAppEnv 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: containerAppEnvName
}

resource appUserAssigned 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-07-31-preview' existing = {
  name: appUserAssignedIdentityName
}

resource acrServiceObj 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: acrService
}

// BUILD ENV Secrets
var secretEnv = [
  {
    name: 'lc-host'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-host'
    identity: appUserAssigned.id
  }
  { 
    name: 'lc-port'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-port'
     identity: appUserAssigned.id 
  }
  {
    name: 'cosmosdbconnectionstring'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/cosmosDbConnectionString'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-domain-client'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-domain-client'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-domain-server'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-domain-server'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-no-index'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-no-index'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-console-json'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-console-json'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-debug-logging'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-debug-logging'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-debug-console'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-debug-console'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-debug-openai'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-debug-openai'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-config-path'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-config-path'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-debug-plugins'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-debug-plugins'
    identity: appUserAssigned.id
  }
  {
    name: 'librechat-creds-key'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/librechat-creds-key'
    identity: appUserAssigned.id
  }
  {
    name: 'librechat-creds-iv'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/librechat-creds-iv'
    identity: appUserAssigned.id
  }
  {
    name: 'librechat-jwt-secret'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/librechat-jwt-secret'
    identity: appUserAssigned.id
  }
  {
    name: 'librechat-jwt-refresh-secret'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/librechat-jwt-refresh-secret'
    identity: appUserAssigned.id
  }
  {
    name: 'librechat-meili-master-key'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/librechat-meili-master-key'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-sd-webui-url'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-sd-webui-url'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-ban-violations'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-ban-violations'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-ban-duration'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-ban-duration'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-ban-interval'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-ban-interval'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-login-violation-score'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-login-violation-score'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-registration-violation-score'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-registration-violation-score'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-concurrent-violation-score'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-concurrent-violation-score'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-message-violation-score'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-message-violation-score'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-non-browser-violation-score'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-non-browser-violation-score'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-login-max'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-login-max'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-login-window'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-login-window'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-register-max'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-register-max'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-register-window'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-register-window'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-limit-concurrent-messages'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-limit-concurrent-messages'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-concurrent-message-max'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-concurrent-message-max'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-limit-message-ip'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-limit-message-ip'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-message-ip-max'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-message-ip-max'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-message-ip-window'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-message-ip-window'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-limit-message-user'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-limit-message-user'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-message-user-max'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-message-user-max'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-message-user-window'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-message-user-window'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-illegal-model-req-score'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-illegal-model-req-score'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-check-balance'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-check-balance'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-email-login'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-email-login'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-registration'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-registration'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-social-login'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-social-login'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-social-registration'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-social-registration'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-password-reset'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-password-reset'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-unverified-email-login'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-unverified-email-login'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-session-expiry'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-session-expiry'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-refresh-token-expiry'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-refresh-token-expiry'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-refresh-token-expiry'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-refresh-token-expiry'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-shared-links'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-shared-links'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-allow-shared-links-public'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-allow-shared-links-public'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-app-title'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-app-title'
    identity: appUserAssigned.id
  }
  {
    name: 'lc-help-and-faq-url'
    keyVaultUrl: '${keyvault.properties.vaultUri}secrets/lc-help-and-faq-url'
    identity: appUserAssigned.id
  }
]
// End Build ENV Secrets

//START ENV values
var envValues = [
  { name: 'MONGO_URI', secretRef: 'cosmosdbconnectionstring' }
  { name: 'DOMAIN_CLIENT', value: 'https://${libreChatContainerService}.${containerAppEnv.properties.defaultDomain}' }
  { name: 'DOMAIN_SERVER', value: 'https://${libreChatContainerService}.${containerAppEnv.properties.defaultDomain}' }
  { name: 'NO_INDEX', secretRef: 'lc-no-index' }
  { name: 'CONSOLE_JSON', secretRef: 'lc-console-json' }
  { name: 'DEBUG_LOGGING', secretRef: 'lc-debug-logging' }
  { name: 'DEBUG_CONSOLE', secretRef: 'lc-debug-console' }
  { name: 'DEBUG_OPENAI', secretRef: 'lc-debug-openai' }
  { name: 'CONFIG_PATH', secretRef: 'lc-config-path' }
  { name: 'DEBUG_PLUGINS', secretRef: 'lc-debug-plugins' }
  { name: 'CREDS_KEY', secretRef: 'librechat-creds-key' }
  { name: 'CREDS_IV', secretRef: 'librechat-creds-iv' }
  { name: 'JWT_SECRET', secretRef: 'librechat-jwt-secret' }
  { name: 'JWT_REFRESH_SECRET', secretRef: 'librechat-jwt-refresh-secret' }
  { name: 'MEILI_MASTER_KEY', secretRef: 'librechat-meili-master-key' }
  { name: 'SD_WEBUI_URL', secretRef: 'lc-sd-webui-url' }
  { name: 'BAN_VIOLATIONS', secretRef: 'lc-ban-violations' }
  { name: 'BAN_DURATION', secretRef: 'lc-ban-duration' }
  { name: 'BAN_INTERVAL', secretRef: 'lc-ban-interval' }
  { name: 'LOGIN_VIOLATION_SCORE', secretRef: 'lc-login-violation-score' }
  { name: 'REGISTRATION_VIOLATION_SCORE', secretRef: 'lc-registration-violation-score' }
  { name: 'CONCURRENT_VIOLATION_SCORE', secretRef: 'lc-concurrent-violation-score' }
  { name: 'MESSAGE_VIOLATION_SCORE', secretRef: 'lc-message-violation-score' }
  { name: 'NON_BROWSER_VIOLATION_SCORE', secretRef: 'lc-non-browser-violation-score' }
  { name: 'LOGIN_MAX', secretRef: 'lc-login-max' }
  { name: 'LOGIN_WINDOW', secretRef: 'lc-login-window' }
  { name: 'REGISTRATION_MAX', secretRef: 'lc-register-max' }
  { name: 'REGISTRATION_WINDOW', secretRef: 'lc-register-window' }
  { name: 'LIMIT_CONCURRENT_MESSAGES', secretRef: 'lc-limit-concurrent-messages' }
  { name: 'CONCURRENT_MESSAGE_MAX', secretRef: 'lc-concurrent-message-max' }
  { name: 'LIMIT_MESSAGE_IP', secretRef: 'lc-limit-message-ip' }
  { name: 'MESSAGE_IP_MAX', secretRef: 'lc-message-ip-max' }
  { name: 'MESSAGE_IP_WINDOW', secretRef: 'lc-message-ip-window' }
  { name: 'LIMIT_MESSAGE_USER', secretRef: 'lc-limit-message-user' }
  { name: 'MESSAGE_USER_MAX', secretRef: 'lc-message-user-max' }
  { name: 'MESSAGE_USER_WINDOW', secretRef: 'lc-message-user-window' }
  { name: 'ILLEGAL_MODEL_REQ_SCORE', secretRef: 'lc-illegal-model-req-score' }
  { name: 'CHECK_BALANCE', secretRef: 'lc-check-balance' }
  { name: 'ALLOW_EMAIL_LOGIN', secretRef: 'lc-allow-email-login' }
  { name: 'ALLOW_REGISTRATION', secretRef: 'lc-allow-registration' }
  { name: 'ALLOW_SOCIAL_LOGIN', secretRef: 'lc-allow-social-login' }
  { name: 'ALLOW_SOCIAL_REGISTRATION', secretRef: 'lc-allow-social-registration' }
  { name: 'ALLOW_PASSWORD_RESET', secretRef: 'lc-allow-password-reset' }
  { name: 'ALLOW_UNVERIFIED_EMAIL_LOGIN', secretRef: 'lc-allow-unverified-email-login' }
  { name: 'SESSION_EXPIRY', secretRef: 'lc-session-expiry' }
  { name: 'REFRESH_TOKEN_EXPIRY', secretRef: 'lc-refresh-token-expiry' }
  { name: 'ALLOW_SHARED_LINKS', secretRef: 'lc-allow-shared-links' }
  { name: 'ALLOW_SHARED_LINKS_PUBLIC', secretRef: 'lc-allow-shared-links-public' }
  { name: 'APP_TITLE', secretRef: 'lc-app-title' }
  { name: 'HELP_AND_FAQ_URL', secretRef: 'lc-help-and-faq-url' }
]

var meilinaVolumes = [
  {
    name: 'meilidata'
    storageType: 'AzureFile'
    storageName: 'file'
  }
]
var meilinaVolumeMounts = [
  {
    volumeName: 'meilidata'
    mountPath: '/meili_data_v1.7'
  }
  {
    volumeName: 'meilidata'
    mountPath: '/config'
  }
]
module meilinaApp 'lcContainerApp.bicep' = {
  name: 'meilisearch'
  params: {
    containerAppEnvName: containerAppEnv.name
    //keyVaultName: keyvault.name
    appUserAssignedIdentityName: appUserAssigned.name
    targetPort: meilinaTargetPort
    minReplicas: minReplicas
    maxReplicas: maxReplicas
    cpuCore: cpuCore
    memorySize: memorySize
    containerImage: meilinaContainerImage
    containerAppName: meilinaAppName
    secretEnv: secretEnv
    envValues: [
      {
        name: 'MEILI_HOST'
        value: 'mydatabase'
      }
      {
        name: 'MEILI_NO_ANALYTICS'
        value: 'true'
      }
      { name: 'EMBEDDINGS_PROVIDER', value: 'azure' }
      { name: 'RAG_AZURE_OPENAI_API_VERSION', value: ragAzureAPIVersion }
      { name: 'EMBEDDINGS_MODEL', value: embeddingsDeployment}
      { name: 'AZURE_OPENAI_API_KEY', value: azureOpenaiApiKey }
      { name: 'AZURE_OPENAI_ENDPOINT', value: azureOpenaiBaseUrl }
      { name: 'RAG_AZURE_OPENAI_ENDPOINT', value: ragAzureOpenaiBaseUrl }
      { name: 'RAG_AZURE_OPENAI_API_KEY', value: ragAzureOpenAIKey }
      ...envValues
    ]
    volumeMounts: meilinaVolumeMounts
    volumes: meilinaVolumes
  }
}

module rag_api 'lcContainerApp.bicep' = {
  name: 'rag-api'
  params: {
    containerAppName: ragApiName
    containerImage: ragApiContainerImage
    appUserAssignedIdentityName: appUserAssigned.name
    targetPort: ragApiTargetPort
    minReplicas: minReplicas
    maxReplicas: maxReplicas
    volumeMounts: [
      {
        volumeName: 'meilidata'
        mountPath: '/config'
      }
    ]
    volumes: meilinaVolumes
    containerAppEnvName: containerAppEnv.name
    secretEnv: [
      {
        name: 'db-host'
        keyVaultUrl: '${keyvault.properties.vaultUri}secrets/db-host'
        identity: appUserAssigned.id
      }
      {
        name: 'pgsqlvector-password-encode'
        keyVaultUrl: '${keyvault.properties.vaultUri}secrets/pgsqlvector-password-encode'
        identity: appUserAssigned.id
      }
      {
        name: 'db-user'
        keyVaultUrl: '${keyvault.properties.vaultUri}secrets/db-user'
        identity: appUserAssigned.id
      }
      {
        name: 'db-vector'
        keyVaultUrl: '${keyvault.properties.vaultUri}secrets/db-vector'
        identity: appUserAssigned.id
      }
      ...secretEnv
    ]
    envValues: [
      { name: 'DB_HOST', secretRef: 'db-host' }
      { name: 'DB_PORT', value: databasePort }
      { name: 'POSTGRES_PASSWORD', secretRef: 'pgsqlvector-password-encode' }
      { name: 'POSTGRES_USER', secretRef: 'db-user' }
      { name: 'POSTGRES_DB', secretRef: 'db-vector' }
      { name: 'RAG_PORT', value: '${ragApiTargetPort}' }
      { name: 'EMBEDDINGS_PROVIDER', value: 'azure' }
      { name: 'RAG_AZURE_OPENAI_API_VERSION', value: ragAzureAPIVersion }
      { name: 'EMBEDDINGS_MODEL', value: embeddingsDeployment}
      { name: 'AZURE_OPENAI_API_KEY', value: azureOpenaiApiKey }
      { name: 'AZURE_OPENAI_ENDPOINT', value: azureOpenaiBaseUrl }
      { name: 'RAG_AZURE_OPENAI_ENDPOINT', value: ragAzureOpenaiBaseUrl }
      { name: 'RAG_AZURE_OPENAI_API_KEY', value: ragAzureOpenAIKey }
      ...envValues
    ]

  }
  dependsOn: [meilinaApp]
}
module api 'lcContainerApp.bicep' = {
  name: libreChatContainerService
  params: {
    containerAppName: libreChatContainerService
    containerAppEnvName: containerAppEnv.name
    appUserAssignedIdentityName: appUserAssigned.name
    containerImage: '${acrServiceObj.properties.loginServer}/${libreChatImage}:${libreChatTag}'
    targetPort: lcTargetPort
    minReplicas: minReplicas
    maxReplicas: maxReplicas
    volumeMounts: [
      {
        volumeName: 'meilidata'
        mountPath: '/config'
      }
    ]
    volumes: meilinaVolumes
    secretEnv: [...secretEnv]
    envValues: [
      { name: 'NODE_ENV', value: 'production'}
      { name: 'MEILI_HOST', value: 'https://${meilinaApp.outputs.container_uri}'}
      { name: 'RAG_PORT', value: '443'}
      { name: 'RAG_API_URL', value: 'https://${rag_api.outputs.container_uri}'}
      
      ...envValues
    ]
  }
}
