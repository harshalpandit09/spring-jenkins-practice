import os
import sys
import subprocess
import glob

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

def main():
    if len(sys.argv) < 4:
        print("Usage: python build_and_push_service.py <build_dir> <service_name> <ecr_repo>")
        sys.exit(1)

    build_dir, service_name, ecr_repo = sys.argv[1], sys.argv[2], sys.argv[3]

    # Find the JAR
    jar_pattern = os.path.join(build_dir, f"{service_name}.*.jar")
    jars = glob.glob(jar_pattern)
    if not jars:
        raise FileNotFoundError(f"No JAR found for {service_name} in {build_dir}")

    jar_path = max(jars, key=os.path.getmtime)  # Latest JAR
    tag = os.path.basename(jar_path).replace(f"{service_name}.", "").replace(".jar", "")

    print(f"Using JAR: {jar_path}")
    print(f"Using tag: {tag}")

    # Copy jar to docker folder
    docker_dir = os.path.join("docker", service_name)
    os.makedirs(docker_dir, exist_ok=True)
    target_jar = os.path.join(docker_dir, f"{service_name}.jar")
    run_cmd(f'copy "{jar_path}" "{target_jar}"')

    # Build Docker image
    run_cmd(f'cd "{docker_dir}" && docker build -t {service_name}:{tag} .')

    # Tag and Push to ECR
    full_image = f"{ecr_repo}/{service_name}:{tag}"
    run_cmd(f"docker tag {service_name}:{tag} {full_image}")
    run_cmd(f"docker push {full_image}")

    print(f"✅ Successfully pushed {full_image}")

if __name__ == "__main__":
    main()
