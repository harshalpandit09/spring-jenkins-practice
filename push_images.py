import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) < 3:
        print("Usage: push_images.py <docker_info_file> <ecr_registry>")
        sys.exit(1)

    docker_info_file = sys.argv[1]
    ecr_registry = sys.argv[2]

    with open(docker_info_file, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for line in lines:
        if ":" not in line:
            continue
        service, tag = line.split(":", 1)
        ecr_image = f"{ecr_registry}/{service}:{tag}"
        print(f"Tagging and pushing {service}:{tag} -> {ecr_image}")
        run_command(f"docker tag {service}:{tag} {ecr_image}")
        run_command(f"docker push {ecr_image}")

if __name__ == "__main__":
    main()
