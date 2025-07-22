import os
import subprocess
import argparse
from datetime import datetime
import shutil

AWS_ACCOUNT_ID = "969258966375"
REGION = "eu-north-1"

# Repositories in ECR
ECR_REPOS = {
    "backend-webapi": "backend-webapi",
    "sql-service": "sql-service",
    "metadata-service": "metadata-service",
}

TEMP_DOCKER_DIR = "D:\\MarketMapBuilds\\docker_temp"


def run_command(cmd):
    """Run a shell command and raise error if it fails."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")


def build_and_push(service_name, build_dir, push_to_ecr):
    """Build and push Docker image for a given service."""
    # Find the latest JAR for this service
    jars = [f for f in os.listdir(build_dir) if f.startswith(service_name) and f.endswith(".jar")]
    if not jars:
        print(f"⚠ No JAR found for {service_name}, skipping.")
        return
    jars.sort(key=lambda f: os.path.getmtime(os.path.join(build_dir, f)), reverse=True)
    jar_name = jars[0]
    print(f"Found latest JAR for {service_name}: {jar_name}")

    # Create temp docker dir
    temp_dir = os.path.join(TEMP_DOCKER_DIR, service_name)
    os.makedirs(temp_dir, exist_ok=True)

    # Copy JAR
    target_path = os.path.join(temp_dir, f"{service_name}.jar")
    shutil.copy(os.path.join(build_dir, jar_name), target_path)
    print(f"Copied JAR to {target_path}")

    # Generate Dockerfile
    dockerfile_path = os.path.join(temp_dir, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(f"FROM openjdk:17-jdk-slim\nWORKDIR /app\nCOPY {service_name}.jar /app/\nENTRYPOINT [\"java\", \"-jar\", \"/app/{service_name}.jar\"]\n")
    print(f"Generated Dockerfile for {service_name} at {dockerfile_path}")

    # Build Docker image
    tag = datetime.now().strftime("%Y%m%d-%H%M%S")
    image_tag = f"{service_name}:{tag}"
    run_command(f'cd "{temp_dir}" && docker build -t {image_tag} .')

    # Push to ECR if required
    if push_to_ecr:
        ecr_image = f"{AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REPOS[service_name]}:{tag}"
        run_command(f"docker tag {image_tag} {ecr_image}")
        run_command(f"docker push {ecr_image}")
        print(f"✅ Pushed {service_name} to {ecr_image}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build_dir", required=True, help="Path to CombinedBuild directory")
    parser.add_argument("--release_version", required=True, help="Release version")
    parser.add_argument("--push_to_ecr", type=str, default="true", help="Push images to ECR (true/false)")
    parser.add_argument("--build_services", type=str, default="true", help="Build backend-webapi")
    parser.add_argument("--build_sql", type=str, default="true", help="Build sql-service")
    parser.add_argument("--build_metadata", type=str, default="true", help="Build metadata-service")
    args = parser.parse_args()

    build_dir = args.build_dir
    push_to_ecr = args.push_to_ecr.lower() == "true"

    # Services to build
    if args.build_services.lower() == "true":
        build_and_push("backend-webapi", build_dir, push_to_ecr)
    if args.build_sql.lower() == "true":
        build_and_push("sql-service", build_dir, push_to_ecr)
    if args.build_metadata.lower() == "true":
        build_and_push("metadata-service", build_dir, push_to_ecr)


if __name__ == "__main__":
    main()
