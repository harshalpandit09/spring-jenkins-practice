import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def push_images(manifest_path, registry, repository):
    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    for line in lines:
        service, version = line.split(':')
        image_tag = f"{registry}/{repository}/{service}:{version}"
        print(f"Tagging and pushing {service}:{version} -> {image_tag}")
        run_command(f"docker tag {service}:{version} {image_tag}")
        run_command(f"docker push {image_tag}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: push_images.py <manifest_path> <registry> <repository>")
        sys.exit(1)

    manifest_path, registry, repository = sys.argv[1], sys.argv[2], sys.argv[3]
    push_images(manifest_path, registry, repository)