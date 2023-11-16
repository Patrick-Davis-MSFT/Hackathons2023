# to run 
# import requirements
# pip install -r ./requirements.txt
# log into azure
# az login
# run the command
# python .\getKeyVaultKey.py -v <vault name> -s <secret name>

import argparse
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient



if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Read a value from Azure Key Vault using the az login Credentials')
    parser.add_argument('-v', '--vaultname', help='Azure Key Value name', required=True)
    parser.add_argument('-s', '--secretname', help='Azure secret name', required=True)
    args = parser.parse_args()
    # Set up the connection to Azure Key Vault
    key_vault_url = "https://" + args.vaultname + ".vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)

    # Retrieve a secret from the key vault
    secret_name = args.secretname
    retrieved_secret = client.get_secret(secret_name)

    # Print the value of the secret
    print(retrieved_secret.value)
