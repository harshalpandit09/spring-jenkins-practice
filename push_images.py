import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python push_images.py <DockerBuildInfo.txt> <AWS_ACCOUNT_ID>")
        sys.exit(1)

    docker_info = sys.argv[1]
    aws_account_id = sys.argv[2]
    region = "eu-north-1"

    with open(docker_info, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # skip comments/empty lines

        if ':' not in line:
            print(f"Skipping invalid line: {line}")
            continue

        service, tag = line.split(":", 1)
        ecr_repo = f"{aws_account_id}.dkr.ecr.{region}.amazonaws.com/{service}:{tag}"

        print(f"Tagging and pushing {service}:{tag} -> {ecr_repo}")
        run_command(f"docker tag {service}:{tag} {ecr_repo}")
        run_command(f"docker push {ecr_repo}")

if __name__ == "__main__":
    main()
