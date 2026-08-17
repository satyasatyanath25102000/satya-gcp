# --------------------------------------------------
# Enable required APIs
# --------------------------------------------------

resource "google_project_service" "container" {
  service = "container.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "artifact_registry" {
  service = "artifactregistry.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_service" "cloud_build" {
  service = "cloudbuild.googleapis.com"

  disable_on_destroy = false
}


# --------------------------------------------------
# Artifact Registry
# --------------------------------------------------

resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "ai-platform"
  description   = "Docker repository for AI Platform"
  format        = "DOCKER"

  depends_on = [
    google_project_service.artifact_registry
  ]
}


# --------------------------------------------------
# GKE Cluster
# --------------------------------------------------

resource "google_container_cluster" "gke" {
  name     = var.cluster_name
  location = var.zone

  depends_on = [
    google_project_service.container
  ]

  # Remove the default node pool.
  # We create our own below.
  remove_default_node_pool = true
  initial_node_count       = 1

  deletion_protection = false

  networking_mode = "VPC_NATIVE"

  ip_allocation_policy {
  }
}


# --------------------------------------------------
# GKE Node Pool
# --------------------------------------------------

resource "google_container_node_pool" "primary" {
  name     = "primary-pool"
  cluster  = google_container_cluster.gke.name
  location = var.zone

  node_count = 1

  node_config {
    machine_type = "e2-medium"

    disk_type    = "pd-standard"
    disk_size_gb = 20

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      workload = "ai-platform"
    }
  }
}
