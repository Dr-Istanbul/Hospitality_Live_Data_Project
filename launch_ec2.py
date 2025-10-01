# scripts/launch_ec2.py
import boto3
import json

def launch_scraping_ec2():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    
    # Use cheapest spot instance
    response = ec2.run_instances(
        ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2023
        InstanceType='t3.medium',
        MinCount=1,
        MaxCount=1,
        InstanceMarketOptions={
            'MarketType': 'spot',
            'SpotOptions': {
                'MaxPrice': '0.02',  # $0.02/hour max
                'SpotInstanceType': 'one-time'
            }
        },
        KeyName='dallas-scraper',  # Your key pair
        SecurityGroupIds=['sg-xxxxxx'],  # Your security group
        IamInstanceProfile={'Name': 'EC2-S3-Access'},
        UserData=user_data_script()  # Setup script below
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Launched EC2 instance: {instance_id}")
    return instance_id

def user_data_script():
    return """#!/bin/bash
    # Update and install dependencies
    yum update -y
    yum install -y python3-pip git
    
    # Clone your scraping code
    git clone https://github.com/yourusername/dallas-scrapers.git
    cd dallas-scrapers
    
    # Install requirements
    pip3 install -r requirements.txt
    
    # Start scraping all three datasets
    python3 scrape_restaurants.py &
    python3 scrape_causes.py &
    python3 scrape_creators.py &
    """