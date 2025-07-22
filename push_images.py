import sys
import subprocess
import os

def run_command(cmd):
    """Run a system command and raise an error if it fails."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) < 4:
        print("Usage: python push_images.py <DockerBuildInfo.txt> <AWS_ACCOUNT_ID> <REGION>")
        sys.exit(1)

    docker_info_file = sys.argv[1]
    aws_account_id = sys.argv[2]
    region = sys.argv[3]
    ecr_base_url = f"{aws_account_id}.dkr.ecr.{region}.amazonaws.com"

    # Mapping local image names to their ECR repository names
    repo_map = {
        "backend-webapi": "backend-webapi",
        "sql-service": "sql-service",
        "metadata-service": "metadata-service"
    }

    # Read DockerBuildInfo.txt
    if not os.path.exists(docker_info_file):
        raise FileNotFoundError(f"{docker_info_file} not found!")

    with open(docker_info_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not lines:
        print("No images found in DockerBuildInfo.txt.")
        return

    print("Images to push:")
    for line in lines:
        print(f" - {line}")

    # Tag and push images
    for line in lines:
        if ':' not in line:
            print(f"Invalid line format: {line}")
            continue

        service, tag = line.split(':', 1)
        if service not in repo_map:
            print(f"Unknown service: {service}")
            continue

        ecr_repo = f"{ecr_base_url}/{repo_map[service]}:{tag}"
        print(f"Tagging and pushing {service}:{tag} -> {ecr_repo}")
        run_command(f"docker tag {service}:{tag} {ecr_repo}")
        run_command(f"docker push {ecr_repo}")

if __name__ == "__main__":
    main()
