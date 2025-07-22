import os
import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python push_images.py <docker_build_info> <aws_account_id>")
        sys.exit(1)

    docker_info_path = sys.argv[1]
    aws_account_id = sys.argv[2]
    region = "eu-north-1"  # Update if region changes

    if not os.path.exists(docker_info_path):
        raise FileNotFoundError(f"Docker build info file not found: {docker_info_path}")

    with open(docker_info_path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not lines:
        print("No Docker images found in DockerBuildInfo.txt")
        return

    for line in lines:
        if ':' not in line:
            continue
        service, tag = line.split(':')
        ecr_repo = f"{aws_account_id}.dkr.ecr.{region}.amazonaws.com/{service}:{tag}"

        print(f"Tagging and pushing {service}:{tag} -> {ecr_repo}")
        run_command(f"docker tag {service}:{tag} {ecr_repo}")
        run_command(f"docker push {ecr_repo}")

if __name__ == "__main__":
    main()
