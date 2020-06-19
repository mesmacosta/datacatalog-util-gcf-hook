# Datacatalog Util Google Cloud Function Hooks

[![License][1]][1] [![Issues][2]][3]

A package to manage Google Cloud Function Hooks.

**Disclaimer: This is not an officially supported Google product.**

<!--
  ⚠️ DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY ️️⚠️
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

## Table of Contents

<!-- toc -->

- [1. Set up Hook](#1-set-up-hook)
  * [1.1 Get the code](#11-get-the-code)
  * [1.2. Set environment variables](#12-set-environment-variables)
  * [1.3. Create Cloud Storage Bucket](#13-create-cloud-storage-bucket)
  * [1.4. Create Service Account](#14-create-service-account)
  * [1.5. Deploy Cloud Function](#15-deploy-cloud-function)
- [2. Test Hook](#2-test-hook)
- [3. Instructions](#3-instructions)

<!-- tocstop -->

-----

## 1. Set up Hook

### 1.1 Get the code

````bash
git clone https://github.com/mesmacosta/datacatalog-util-gcf-hook/
cd datacatalog-util-gcf-hook
````
Run the following commands inside datacatalog-util-gcf-hook directory.

### 1.2. Set environment variables

Replace below values according to your environment:

```bash
export PROJECT_ID=$(gcloud config get-value project)
export DATACATALOG_UTIL_GCF_HOOK_SA_NAME="datacatalog-util-gcs-hook-sa"
export DATACATALOG_UTIL_GCF_HOOK_SA_EMAIL="$DATACATALOG_UTIL_GCF_HOOK_SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"
export DATACATALOG_UTIL_BUCKET_HOOK="datacatalog-util-$PROJECT_ID"
export DATACATALOG_UTIL_HOOK_TYPE="hooks/tag-templates"
```

### 1.3. Create Cloud Storage Bucket
Create a Cloud Storage bucket
```bash
function_suffix=$DATACATALOG_UTIL_HOOK_TYPE
# Replace / to -
function_suffix=${function_suffix////-}
export BUCKET_NAME="$DATACATALOG_UTIL_BUCKET_HOOK-$function_suffix"
gsutil mb "gs://$BUCKET_NAME/"
```

### 1.4. Create Service Account
```bash
gcloud iam service-accounts create $DATACATALOG_UTIL_GCF_HOOK_SA_NAME \
--display-name  "Service Account for Data Catalog Util HOOKS" \
--project $PROJECT_ID
```

Next add Data Catalog admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:$DATACATALOG_UTIL_GCF_HOOK_SA_EMAIL" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"
```

Next add Log writer role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:$DATACATALOG_UTIL_GCF_HOOK_SA_EMAIL" \
--quiet \
--project $PROJECT_ID \
--role "roles/logging.logWriter"
```

Next add Storage Viewer role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:$DATACATALOG_UTIL_GCF_HOOK_SA_EMAIL" \
--quiet \
--project $PROJECT_ID \
--role "roles/storage.objectViewer"
```

### 1.5. Deploy Cloud Function

- Python + virtualenv

```bash
gcloud functions deploy "$BUCKET_NAME-gcf" \
 --runtime python37 \
 --trigger-resource $BUCKET_NAME  \
 --trigger-event google.storage.object.finalize \
 --service-account $DATACATALOG_UTIL_GCF_HOOK_SA_EMAIL \
 --source $DATACATALOG_UTIL_HOOK_TYPE \
 --entry-point run
```

## 2. Test Hook
```bash
gsutil cp sample-input/create-tag-templates/datacatalog-sync-tag-templates-1.csv "gs://$BUCKET_NAME/"
```

## 3. Instructions
Hooks trigger `datacatalog-util` commands when the configured `file_pattern` is uploaded in the bucket.

| Hook                     |  Description                              | File Pattern                         |
| ---                      | ---                                       | ---                                  |
| **hooks/tag-templates**  | Automated Tag Templates CSV ingestion.    | datacatalog-sync-tag-templates-*.csv |


[1]: https://img.shields.io/github/license/mesmacosta/datacatalog-util-gcf-hook.svg
[2]: https://img.shields.io/github/issues/mesmacosta/datacatalog-util-gcf-hook.svg
[3]: https://github.com/mesmacosta/datacatalog-util-gcf-hook/issues
