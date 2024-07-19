terraform {
  required_providers {
    lxd = {
      source = "terraform-lxd/lxd"
      version = "2.1.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}
