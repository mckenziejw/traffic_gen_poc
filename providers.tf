terraform {
  required_providers {
    lxd = {
      source = "terraform-lxd/lxd"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}
