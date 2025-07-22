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

        service, tag = line.strip().split(":")
        service = service.strip()
        tag = tag.strip()

        # Map each service to its ECR repo
        ecr_repo_name = service
        ecr_image = f"{account_id}.dkr.ecr.{region}.amazonaws.com/{ecr_repo_name}:{tag}"

        print(f"Tagging and pushing {service}:{tag} -> {ecr_image}")
        run_command(f"docker tag {service}:{tag} {ecr_image}")
        run_command(f"docker push {ecr_image}")

if __name__ == "__main__":
    main()