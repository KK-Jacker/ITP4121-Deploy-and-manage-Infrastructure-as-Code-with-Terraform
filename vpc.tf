variable "project_id" {
  description = "project id"
}

variable "region" {
  description = "region"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_network" "vpc" {
  name                    = "${var.project_id}-vpc"
  auto_create_subnetworks = "false"
}

resource "google_compute_subnetwork" "subnet1" {
  name          = "${var.project_id}-subnet1"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.1.0.0/16"
}
resource "google_compute_subnetwork" "subnet2" {
  name          = "${var.project_id}-subnet2"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.2.0.0/16"
}
