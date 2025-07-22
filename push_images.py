import subprocess
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

if len(sys.argv) != 4:
    print("Usage: python push_images.py <docker_info_file> <ecr_registry> <ecr_repo>")
    sys.exit(1)

docker_info_file = sys.argv[1]
ecr_registry = sys.argv[2]
ecr_repo = sys.argv[3]

with open(docker_info_file, 'r') as f:
    lines = [line.strip() for line in f if not line.startswith("#")]

for line in lines:
    service, version = line.split(":")
    image_name = f"{service}:{version}"
    ecr_image = f"{ecr_registry}/{ecr_repo}/{service}:{version}"
    print(f"Tagging and pushing {image_name} -> {ecr_image}")
    run_command(f"docker tag {image_name} {ecr_image}")
    run_command(f"docker push {ecr_image}")