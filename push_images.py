import os
import subprocess
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) < 3:
        print("Usage: push_images.py <docker_info_file> <aws_account_id>")
        sys.exit(1)

    docker_info_file = sys.argv[1]
    aws_account_id = sys.argv[2]
    region = "eu-north-1"

    # Read all images from DockerBuildInfo.txt
    if not os.path.exists(docker_info_file):
        print(f"Error: {docker_info_file} not found")
        sys.exit(1)

    with open(docker_info_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not lines:
        print(f"No images found in {docker_info_file}")
        sys.exit(1)

    for line in lines:
        try:
            service, tag = line.split(":")
            ecr_image = f"{aws_account_id}.dkr.ecr.{region}.amazonaws.com/{service}:{tag}"
            print(f"Tagging and pushing {service}:{tag} -> {ecr_image}")
            run_command(f"docker tag {service}:{tag} {ecr_image}")
            run_command(f"docker push {ecr_image}")
        except ValueError:
            print(f"Skipping invalid line in {docker_info_file}: {line}")

if __name__ == "__main__":
    main()
