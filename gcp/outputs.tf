output "region" {
  value       = var.region
  description = "GCloud Region"
}

output "project_id" {
  value       = var.project_id
  description = "GCloud Project ID"
}

output "kubernetes_cluster_name" {
  value       = google_container_cluster.primary.name
  description = "GKE Cluster Name"
}

output "kubernetes_cluster_host" {
  value       = google_container_cluster.primary.endpoint
  description = "GKE Cluster Host"
}

output "kubernetes_cluster_ID" {
  value       = google_container_cluster.primary.id
  description = "GKE Cluster ID"
}

output "kubernetes_cluster_zone" {
  value = google_container_cluster.primary.node_locations
}

output "kubernetes_cluster_cluster_ca_certificate" {
  value = google_container_cluster.primary.master_auth.0.cluster_ca_certificate
  sensitive = true
}

output "kubernetes_cluster_cluster_host" {
  value = module.gke_auth.host

}

output "kubernetes_cluster_cluster_token" {
  value = module.gke_auth.token
  sensitive = true
}