import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) < 3:
        print("Usage: push_images.py <DockerBuildInfo.txt> <ECR_BASE>")
        sys.exit(1)

    manifest_file = sys.argv[1]
    ecr_base = sys.argv[2]

    with open(manifest_file, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for line in lines:
        service, tag = line.split(":")
        ecr_repo = f"{ecr_base}/{service}:{tag}"
        print(f"Tagging and pushing {service}:{tag} -> {ecr_repo}")
        run_command(f"docker tag {service}:{tag} {ecr_repo}")
        run_command(f"docker push {ecr_repo}")

if __name__ == "__main__":
    main()