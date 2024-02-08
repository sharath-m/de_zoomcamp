variable "credentials" {
  default = "./keys/my-creds.json"
}

variable "project" {
  default = "de-zoom-terrform"
}

variable "region" {
  default = "us-central1"
}

variable "location" {
  default = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery dataset name"
  default = "demo_dataset"
}
variable "gcs_bucket_name" {
  description = "Storage Bucket Name"
  default = "de-zoom-terrform-demo-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default = "STANDARD"
}