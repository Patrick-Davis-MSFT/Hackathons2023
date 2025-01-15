"""
This script performs OCR on a document using Azure Computer Vision.

Usage:
    python ocr-document.py -e <endpoint> -k <key> -d <document_path>

Arguments:
    -e, --endpoint   Azure Computer Vision endpoint (required)
    -k, --key        Azure Computer Vision key (required)
    -d, --document   Path to the document to analyze (required)

Example:
    python ocr-document.py -e https://<your-endpoint>.cognitiveservices.azure.com/ -k <your-key> -d /path/to/document.pdf

Ensure you have the required packages installed by using the requirements.txt file:
    pip install -r requirements.txt


"""

import argparse
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def analyze_document(endpoint, key, document_path):
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    with open(document_path, "rb") as document:
        poller = client.begin_analyze_document("prebuilt-read", document)
        result = poller.result()
    print("Document was analyzed")
    for page in result.pages:
        for line in page.lines:
            print(line.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform OCR on a document using Azure Computer Vision')
    parser.add_argument('-e', '--endpoint', help='Azure Computer Vision endpoint', required=True)
    parser.add_argument('-k', '--key', help='Azure Computer Vision key', required=True)
    parser.add_argument('-d', '--document', help='Path to the document to analyze', required=True)
    args = parser.parse_args()

    analyze_document(args.endpoint, args.key, args.document)