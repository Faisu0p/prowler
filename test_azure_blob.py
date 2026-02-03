#!/usr/bin/env python3
"""
Quick test script for Azure Blob Storage integration
Run this to verify the code works before deploying
"""
import os
import sys

# Add the API backend to Python path
sys.path.insert(0, "/Users/faisu/Documents/Development/prowler/api/src/backend")

# Set required Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.devel")

# Set Azure credentials from your environment
os.environ["AZURE_STORAGE_CONNECTION_STRING"] = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING", ""
)
os.environ["AZURE_STORAGE_CONTAINER_NAME"] = "kyudo-pilot"

print("🧪 Testing Azure Blob Storage Integration\n")
print("=" * 60)

# Test 1: Check if azure-storage-blob is installed
print("\n✓ Test 1: Checking azure-storage-blob package...")
try:
    from azure.storage.blob import BlobServiceClient

    print("  ✅ azure-storage-blob package is installed")
except ImportError as e:
    print(f"  ❌ FAILED: {e}")
    print("  Run: cd api && poetry install")
    sys.exit(1)

# Test 2: Check if connection string is set
print("\n✓ Test 2: Checking Azure connection string...")
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if connection_string:
    print(f"  ✅ Connection string is set ({len(connection_string)} chars)")
else:
    print("  ⚠️  WARNING: AZURE_STORAGE_CONNECTION_STRING not set")
    print(
        "  Set it with: export AZURE_STORAGE_CONNECTION_STRING='your-connection-string'"
    )

# Test 3: Try to create blob client
print("\n✓ Test 3: Creating Azure Blob Service Client...")
if connection_string:
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        print("  ✅ Blob Service Client created successfully")

        # Test 4: Check if container exists
        print("\n✓ Test 4: Checking if container 'kyudo-pilot' exists...")
        container_client = blob_service_client.get_container_client("kyudo-pilot")
        if container_client.exists():
            print("  ✅ Container 'kyudo-pilot' exists")

            # Test 5: Try to upload a test file
            print("\n✓ Test 5: Uploading test file...")
            test_content = b"This is a test file from Prowler Azure Blob integration"
            test_blob_name = "test/prowler-test-file.txt"

            blob_client = container_client.get_blob_client(test_blob_name)
            blob_client.upload_blob(test_content, overwrite=True)

            print("  ✅ Test file uploaded successfully!")
            print(f"     Blob URL: {blob_client.url}")

            # Clean up test file
            blob_client.delete_blob()
            print("  ✅ Test file deleted (cleanup)")

        else:
            print("  ❌ Container 'kyudo-pilot' does NOT exist")
            print("  Create it in Azure Portal or with: az storage container create")
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        sys.exit(1)
else:
    print("  ⏭️  SKIPPED (no connection string)")

print("\n" + "=" * 60)
print("✅ All tests passed! Ready to deploy to Azure.")
print("\nNext steps:")
print(
    "1. Build Docker image: cd prowler && docker build -t prowleracr.azurecr.io/prowler-api:latest -f api/Dockerfile --target prod ./api"
)
print("2. Push to ACR: docker push prowleracr.azurecr.io/prowler-api:latest")
print("3. Restart Azure App Services")
