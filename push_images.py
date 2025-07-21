import subprocess
import sys
import os

if len(sys.argv) != 4:
    print("Usage: python push_images.py <DOCKER_MANIFEST> <ECR_REGISTRY> <ECR_REPO>")
    sys.exit(1)

DOCKER_MANIFEST = sys.argv[1]
ECR_REGISTRY = sys.argv[2]
ECR_REPO = sys.argv[3]

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

if not os.path.exists(DOCKER_MANIFEST):
    print(f"Error: Docker manifest file not found at {DOCKER_MANIFEST}")
    sys.exit(1)

with open(DOCKER_MANIFEST, "r") as f:
    lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

for line in lines:
    if ":" not in line:
        print(f"Skipping invalid line: {line}")
        continue
    service, version = line.split(":", 1)
    service = service.strip()
    version = version.strip()
    image_tag = f"{ECR_REGISTRY}/{ECR_REPO}/{service}-{version}"

    print(f"Tagging and pushing {service}:{version} -> {image_tag}")
    run_command(f"docker tag {service}:{version} {image_tag}")
    run_command(f"docker push {image_tag}")