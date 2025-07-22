import subprocess
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python push_images.py <docker_build_info_path> <aws_account_id>")
        sys.exit(1)

    docker_info_file = sys.argv[1]
    account_id = sys.argv[2]
    region = "eu-north-1"

    with open(docker_info_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#") or not line.strip():
            continue

        # Split the service and tag
        service, tag = line.strip().split(":")
        service = service.strip()
        tag = tag.strip()

        # Construct ECR repo URL
        ecr_repo = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{service}:{tag}"
        print(f"Tagging and pushing {service}:{tag} -> {ecr_repo}")

        run_command(f"docker tag {service}:{tag} {ecr_repo}")
        run_command(f"docker push {ecr_repo}")

if __name__ == "__main__":
    main()