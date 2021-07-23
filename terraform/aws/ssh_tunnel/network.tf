# Setting up subnets within our main vpc, for ssh tunnel testing.
# We need an ec2 instance (bastion host) reachable from the net with port 22 open for inbound ssh.
# The ec2 instance should be able to download package updates from the public internet, for ease of setup.
# We need a postgres instance NOT reachable from the net, but YES reachable from the EC2 instance. Fake data is generated by unit tests.
# The subnets here should not have access to any other part of airbyte infrastructure; they should remain isolated.


data "aws_vpc" "main" {
  id = "vpc-001ad881b80193126"
}
data "aws_internet_gateway" "default" {
  filter {
    name   = "attachment.vpc-id"
    values = [data.aws_vpc.main.id]
  }
}

resource "aws_subnet" "main-subnet-public-dbtunnel" {
    vpc_id = data.aws_vpc.main.id
    cidr_block = "10.0.40.0/24"
    map_public_ip_on_launch = "true" 
    availability_zone = "us-east-2a"
    tags = {
        Name = "public-dbtunnel"
    }
}

resource "aws_route_table" "dbtunnel-public-route" {
    vpc_id = data.aws_vpc.main.id
    
    route {
        //associated subnet can reach everywhere
        cidr_block = "0.0.0.0/0" 
        //uses this to reach internet
        gateway_id = data.aws_internet_gateway.default.id
    }
    
    tags = {
        Name = "dbtunnel-public-route"
    }
}

resource "aws_route_table_association" "dbtunnel-route-assoc-public-subnet-1"{
    subnet_id = "${aws_subnet.main-subnet-public-dbtunnel.id}"
    route_table_id = "${aws_route_table.dbtunnel-public-route.id}"
}

