import sys
import subprocess
import os

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python push_images.py <DockerBuildInfo.txt> <ECR_URL>")
        sys.exit(1)

    build_info_file = sys.argv[1]
    ecr_url = sys.argv[2]

    if not os.path.exists(build_info_file):
        print(f"Error: {build_info_file} does not exist.")
        sys.exit(1)

    with open(build_info_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    if not lines:
        print("No images to push found in DockerBuildInfo.txt.")
        sys.exit(0)

    for line in lines:
        if ':' not in line:
            print(f"Skipping invalid line: {line}")
            continue
        service, tag = line.split(':', 1)
        ecr_image = f"{ecr_url}/{service}:{tag}"
        print(f"Tagging and pushing {service}:{tag} -> {ecr_image}")

        # Tag and push
        run_command(f"docker tag {service}:{tag} {ecr_image}")
        run_command(f"docker push {ecr_image}")

if __name__ == "__main__":
    main()
