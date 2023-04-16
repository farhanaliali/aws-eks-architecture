from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EKS, EC2Instance, ECR
from diagrams.aws.network import NATGateway, VPCElasticNetworkInterface, InternetGateway
from diagrams.aws.security import IAM, IAMRole
from diagrams.k8s.rbac import User


with Diagram("AWS EKS environment", outformat="png", direction="TB"):
  with Cluster("AWS Cloud"):
    with Cluster("VPC Amazon EKS"):
       ekscp = EKS("EKS Control plane")
    with Cluster("VPC Cloud environment"):
      with Cluster("Availability Zone 1"):
        with Cluster("Public Subnet"):
           nat = NATGateway("NAT GATEWAY")
           eniavz1 = VPCElasticNetworkInterface("EKS Elastic Network Interface")
           ec2pubavz1 = EC2Instance("EKS Worker Node")
        with Cluster("Private Subnet"):
           ec2privavz1 = EC2Instance("EKS Worker Node")
    
      with Cluster("Availability Zone 2"):
        with Cluster("Public Subnet"):
           ec2bastpubavz2 = EC2Instance("Bastion EC2 Instance")
           eniavz2 = VPCElasticNetworkInterface("EKS Elastic Network Interface")
           ec2pubavz2 = EC2Instance("EKS Worker Node")
        with Cluster("Private Subnet"):
           ec2privavz2 = EC2Instance("EKS Worker Node")
      InternetGateway("Internet Gateway")
 
    usr = User("Admin")
    ECR("Elastic Container Registry")
    iamserv = IAM("Identity Management")
    additroles = [IAMRole("Role for EKS Cluster"), IAMRole("Role for EKS Node Groups")]

    eniavz1 - Edge(color="blue", style="dashed", label="EKS Cluster SG") - eniavz2
    pubngsg = ec2pubavz1 - Edge(color="orange", style="dashed", label="Public Node Group SG") - ec2pubavz2
    ec2privavz1 - Edge(color="orange", style="dashed", label="Private NG SG") - ec2privavz2
    ec2privavz1 >> nat << ec2privavz2
    nat >> ekscp 
    eniavz1 >> ekscp << eniavz2
    ec2pubavz1 >> ekscp << ec2pubavz2
    usr >> ec2bastpubavz2
    iamserv >> additroles
