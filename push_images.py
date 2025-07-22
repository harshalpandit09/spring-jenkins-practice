import subprocess
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def push_images(manifest_file, ecr_registry, ecr_repo):
    with open(manifest_file, "r") as f:
        lines = [line.strip() for line in f if not line.startswith("#") and line.strip()]

    for line in lines:
        service, version = line.split(":")
        ecr_image = f"{ecr_registry}/{ecr_repo}:{service}-{version}"
        print(f"Tagging and pushing {service}:{version} -> {ecr_image}")
        run_command(f"docker tag {service}:{version} {ecr_image}")
        run_command(f"docker push {ecr_image}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: push_images.py <manifest_file> <ecr_registry> <ecr_repo>")
        sys.exit(1)

    manifest_file = sys.argv[1]
    ecr_registry = sys.argv[2]
    ecr_repo = sys.argv[3]
    push_images(manifest_file, ecr_registry, ecr_repo)