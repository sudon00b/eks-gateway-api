variable "image_tag_mutability" {
   default = "MUTABLE"
}

variable "scan_on_push" {
  default = true
}


variable "region" {
  default = "ap-south-1"
  
}

variable "project_name" {
    type = string
  
}
variable "newrelic_license_key" {
  type        = string
  description = "New Relic license key"
  sensitive   = true
}

