# Azure Blob Storage Integration - Deployment Guide

## Changes Made

### 1. Code Changes

**Files Modified:**

- `api/pyproject.toml` - Added `azure-storage-blob` dependency
- `api/src/backend/tasks/jobs/export.py` - Added Azure Blob upload functions
- `api/src/backend/config/django/base.py` - Added Azure storage configuration
- `api/src/backend/tasks/tasks.py` - Exported new upload function

**New Functions:**

- `get_azure_blob_client()` - Creates Azure Blob Service Client
- `_upload_to_azure_blob()` - Uploads files to Azure Blob Storage
- `_upload_artifact()` - Smart upload function (tries Azure first, falls back to S3)

### 2. Azure Configuration (Already Done by You)

✅ Added environment variables to App Services:

- `AZURE_STORAGE_CONNECTION_STRING`
- `AZURE_STORAGE_CONTAINER_NAME=kyudo-pilot`

## Deployment Steps

### Step 1: Install New Dependencies

```bash
cd /Users/faisu/Documents/Development/prowler/api
poetry install
```

### Step 2: Build and Push Docker Images

```bash
# Set variables
RESOURCE_GROUP="kyudo_dev"
ACR_NAME="prowleracr"
ACR_LOGIN_SERVER="prowleracr.azurecr.io"

# Login to ACR
az acr login --name $ACR_NAME

# Build and push API image (includes worker)
cd /Users/faisu/Documents/Development/prowler
docker build -t $ACR_LOGIN_SERVER/prowler-api:latest -f api/Dockerfile --target prod ./api
docker push $ACR_LOGIN_SERVER/prowler-api:latest
```

### Step 3: Restart App Services

```bash
# Restart API
az webapp restart --name prowler-api-dev --resource-group kyudo_dev

# Restart Worker
az webapp restart --name prowler-worker --resource-group kyudo_dev
```

### Step 4: Verify Deployment

1. **Check API Logs:**

```bash
az webapp log tail --name prowler-api-dev --resource-group kyudo_dev
```

2. **Check Worker Logs:**

```bash
az webapp log tail --name prowler-worker --resource-group kyudo_dev
```

3. **Trigger a Test Scan** and verify:
   - Scan completes successfully
   - Reports are uploaded to Azure Blob Storage (check `kyudo-pilot` container)
   - Download links work from the UI

### Step 5: Verify Azure Blob Storage

```bash
# List blobs in container
az storage blob list \
  --account-name lrstoragefile \
  --container-name kyudo-pilot \
  --output table
```

You should see files with structure:

```
{tenant_id}/{scan_id}/{filename}.zip
```

## How It Works

1. **Priority**: The code checks for Azure Blob configuration first
2. **Fallback**: If Azure is not configured, it falls back to S3
3. **Scan Workflow**:
   - Worker generates scan reports locally
   - Reports are compressed into a ZIP file
   - `_upload_artifact()` is called
   - Files are uploaded to Azure Blob Storage
   - Blob URL is stored in the database
   - UI can download from the blob URL

## Troubleshooting

### Issue: "azure-storage-blob module not found"

**Solution:** Run `poetry install` in the api directory and rebuild Docker images

### Issue: "AZURE_STORAGE_CONNECTION_STRING not configured"

**Solution:** Verify environment variable is set in App Service configuration

### Issue: Uploads still going to S3

**Solution:** Azure connection string must be set. Check the priority logic in `_upload_artifact()`

### Issue: "Container does not exist"

**Solution:** Verify `kyudo-pilot` container exists in storage account

## Testing Locally

Before deploying, you can test locally:

```bash
# Set env vars locally
export AZURE_STORAGE_CONNECTION_STRING="your-connection-string"
export AZURE_STORAGE_CONTAINER_NAME="kyudo-pilot"

# Run API locally
cd api
poetry shell
python manage.py runserver

# In another terminal, run worker
cd api
poetry shell
celery -A config.celery.app worker -l INFO
```

## Monitoring

After deployment, monitor:

- App Service logs for upload success/failure messages
- Azure Storage account metrics (transactions, ingress)
- Scan completion times
- Download link functionality in UI

## Rollback Plan

If issues occur:

1. Stop new deployments
2. Revert to previous Docker image:

```bash
az webapp config container set \
  --name prowler-api-dev \
  --resource-group kyudo_dev \
  --docker-custom-image-name prowleracr.azurecr.io/prowler-api:previous-tag
```

3. Remove Azure environment variables temporarily
4. Reports will fall back to local storage
