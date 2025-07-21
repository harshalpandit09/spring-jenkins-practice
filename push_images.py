import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def push_images(manifest_path, ecr_registry, repository):
    with open(manifest_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue  # Skip comments or empty lines

        if ":" not in line:
            print(f"Skipping invalid line: {line}")
            continue

        service, version = line.split(":")
        local_tag = f"{service}:{version}"
        ecr_tag = f"{ecr_registry}/{repository}:{service}-{version}"

        print(f"Tagging and pushing {local_tag} -> {ecr_tag}")
        run_command(f"docker tag {local_tag} {ecr_tag}")
        run_command(f"docker push {ecr_tag}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python push_images.py <manifest_file> <ecr_registry> <repository>")
        sys.exit(1)

    manifest_path = sys.argv[1]
    ecr_registry = sys.argv[2]
    repository = sys.argv[3]

    push_images(manifest_path, ecr_registry, repository)