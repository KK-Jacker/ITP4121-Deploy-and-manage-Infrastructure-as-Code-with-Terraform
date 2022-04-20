## GCP Resources

data "terraform_remote_state" "eks" {
  backend = "local"
  config = {
    path = "../gcp/terraform.tfstate"
  }
}
data "google_client_config" "provider" {}



provider "google" {
  region = data.terraform_remote_state.eks.outputs.region
}

data "google_container_cluster" "cluster" {
  name = data.terraform_remote_state.eks.outputs.kubernetes_cluster_ID
  location = data.terraform_remote_state.eks.outputs.region
  project = "perceptive-map-347614"
}

provider "kubernetes" {
  alias                  = "eks"
  host                   = "https://${data.terraform_remote_state.eks.outputs.kubernetes_cluster_host}"
  cluster_ca_certificate = base64decode(data.terraform_remote_state.eks.outputs.kubernetes_cluster_cluster_ca_certificate)
  //token                  = data.terraform_remote_state.gcp.outputs.kubernetes_cluster_cluster_token
  config_path = "~/.kube/config"

  experiments {
    manifest_resource = true
  }
}

provider "helm" {
  alias = "eks"
  kubernetes {
    host                   = "https://${data.terraform_remote_state.eks.outputs.kubernetes_cluster_host}"
    cluster_ca_certificate = base64decode(data.terraform_remote_state.eks.outputs.kubernetes_cluster_cluster_ca_certificate)
    //token                  = data.terraform_remote_state.gcp.outputs.kubernetes_cluster_cluster_token
    config_path = "~/.kube/config"

  }
}

resource "helm_release" "consul_dc1" {
  provider   = helm.eks
  name       = "consul"
  repository = "https://helm.releases.hashicorp.com"
  chart      = "consul"
  version    = "0.32.1"


  values = [
    file("dc1.yaml")
  ]
}

data "kubernetes_secret" "eks_federation_secret" {
  provider = kubernetes.eks
  metadata {
    name = "consul-federation"
  }

  depends_on = [helm_release.consul_dc1]
}

## Azure Resources

data "terraform_remote_state" "aks" {
  backend = "local"
  config = {
    path = "../Azure/terraform.ITP4121-Project.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_kubernetes_cluster" "cluster" {
  name                = data.terraform_remote_state.aks.outputs.kubernetesclustername
  resource_group_name = data.terraform_remote_state.aks.outputs.resourcegroupname
}

provider "kubernetes" {
  alias                  = "aks"
  host                   = data.azurerm_kubernetes_cluster.cluster.kube_config.0.host
  client_certificate     = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate)
  client_key             = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate)

  experiments {
    manifest_resource = true
  }
}

provider "helm" {
  alias = "aks"
  kubernetes {
    host                   = data.azurerm_kubernetes_cluster.cluster.kube_config.0.host
    client_certificate     = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate)
    client_key             = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(data.azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate)
  }
}

resource "kubernetes_secret" "aks_federation_secret" {
  provider = kubernetes.aks
  metadata {
    name = "consul-federation"
  }

  data = data.kubernetes_secret.eks_federation_secret.data
}


resource "helm_release" "consul_dc2" {
  provider   = helm.aks
  name       = "consul"
  repository = "https://helm.releases.hashicorp.com"
  chart      = "consul"
  version    = "0.32.1"

  values = [
    file("dc2.yaml")
  ]

  depends_on = [kubernetes_secret.aks_federation_secret]
}
