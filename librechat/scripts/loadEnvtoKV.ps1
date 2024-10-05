param (
    [string]$envFilePath,
    [string]$keyVaultName
)

# Function to read .env file and return a hashtable of key-value pairs
function Read-EnvFile {
    param (
        [string]$filePath
    )

    $envVars = @{}
    $lines = Get-Content -Path $filePath

    foreach ($line in $lines) {
        if ($line -match '^\s*#') {
            continue
        }

        if ($line -match '^\s*([^=]+)\s*=\s*(.*)\s*$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $envVars[$key] = $value
        }
    }

    return $envVars
}

# Function to write secrets to Azure Key Vault
function Write-SecretsToKeyVault {
    param (
        [hashtable]$secrets,
        [string]$keyVaultName
    )

    foreach ($key in $secrets.Keys) {
        $value = $secrets[$key]
        $formattedKey = 'lc-' + $key.ToLower() -replace '_', '-'
        Write-Host "Setting secret $key ($formattedKey) in Key Vault $keyVaultName"
        # Write-Host "Value: $value"
        # Write-Host "az keyvault secret set --vault-name $keyVaultName --name $formattedKey --value $value"
        az keyvault secret set --vault-name "$keyVaultName" --name "$formattedKey" --value "$value" | Out-Null
    }
}

# Main script
if (-Not (Test-Path -Path $envFilePath)) {
    Write-Host "The specified .env file does not exist: $envFilePath"
    exit 1
}

$envVars = Read-EnvFile -filePath $envFilePath
Write-SecretsToKeyVault -secrets $envVars -keyVaultName $keyVaultName

Write-Host "All secrets have been set in Key Vault $keyVaultName"