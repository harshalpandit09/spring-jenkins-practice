import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

if len(sys.argv) != 4:
    print("Usage: python push_images.py <docker_manifest_file> <ecr_registry> <ecr_repository>")
    sys.exit(1)

manifest_file = sys.argv[1]
ecr_registry = sys.argv[2]
ecr_repository = sys.argv[3]

with open(manifest_file, 'r') as f:
    lines = f.readlines()

for line in lines:
    if line.startswith("#") or ":" not in line:
        continue

    service, version = line.strip().split(":")
    full_tag = f"{service}-{version}"
    image_tag = f"{ecr_registry}/{ecr_repository}:{full_tag}"

    print(f"Tagging and pushing {service}:{version} -> {image_tag}")
    run_command(f"docker tag {service}:{version} {image_tag}")
    run_command(f"docker push {image_tag}")