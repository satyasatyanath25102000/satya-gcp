output "cluster_name" {
  value = google_container_cluster.gke.name
}

output "cluster_location" {
  value = google_container_cluster.gke.location
}

output "artifact_registry" {
  value = google_artifact_registry_repository.docker_repo.name
}
