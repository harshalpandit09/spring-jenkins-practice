import os
import sys
import subprocess
import shutil

AWS_ACCOUNT_ID = "969258966375"
REGION = "eu-north-1"

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.check_call(cmd, shell=True)

def build_and_push(component, release_version, push_to_ecr):
    build_dir = f"D:\\MarketMapBuilds\\{release_version}\\CombinedBuild"
    docker_context = f"C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\MarketMap-Docker-Packaging\\docker\\{component}"
    ecr_repo = f"{AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{component}"

    # Find latest JAR
    jars = [f for f in os.listdir(build_dir) if f.startswith(component) and f.endswith(".jar")]
    if not jars:
        raise FileNotFoundError(f"No {component} JAR found in {build_dir}")

    jars.sort(key=lambda x: os.path.getmtime(os.path.join(build_dir, x)), reverse=True)
    latest_jar = jars[0]
    tag = latest_jar.replace(f"{component}.", "").replace(".jar", "")
    print(f"Found JAR: {latest_jar}")
    print(f"Using Docker tag: {tag}")

    # Copy JAR
    target_jar = os.path.join(docker_context, f"{component}.jar")
    shutil.copy(os.path.join(build_dir, latest_jar), target_jar)

    # Build Docker image
    run(f'docker build --platform linux/amd64 -t {component}:{tag} "{docker_context}"')

    # Push to ECR
    if push_to_ecr.lower() == "true":
        run(f'docker tag {component}:{tag} {ecr_repo}:{tag}')
        run(f'docker push {ecr_repo}:{tag}')

def main():
    if len(sys.argv) < 4:
        print("Usage: python build_push_backend.py <component> <release_version> <push_to_ecr>")
        sys.exit(1)

    build_and_push(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
