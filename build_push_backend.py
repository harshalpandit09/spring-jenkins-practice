import os
import subprocess
import shutil
import sys

AWS_ACCOUNT_ID = "969258966375"
REGION = "eu-north-1"

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.check_call(cmd, shell=True)

def build_and_push(component, release_version, push_to_ecr):
    build_dir = f"D:\\MarketMapBuilds\\{release_version}\\CombinedBuild"
    docker_context = f"C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\MarketMap-Docker-Packaging\\docker\\{component}"
    ecr_repo = f"{AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{component}"

    jars = [f for f in os.listdir(build_dir) if f.startswith(component) and f.endswith(".jar")]
    if not jars:
        raise FileNotFoundError(f"No {component} JAR found in {build_dir}")
    jars.sort(key=lambda x: os.path.getmtime(os.path.join(build_dir, x)), reverse=True)
    latest_jar = jars[0]
    tag = latest_jar.replace(f"{component}.", "").replace(".jar", "")

    print(f"Found JAR: {latest_jar}")
    print(f"Using Docker tag: {tag}")

    shutil.copy(os.path.join(build_dir, latest_jar), os.path.join(docker_context, f"{component}.jar"))

    run(f'docker build --platform linux/amd64 -t {component}:{tag} "{docker_context}"')

    if push_to_ecr.lower() == "true":
        run(f'aws ecr get-login-password --region {REGION} | docker login --username AWS --password-stdin {AWS_ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com')
        run(f'docker tag {component}:{tag} {ecr_repo}:{tag}')
        run(f'docker push {ecr_repo}:{tag}')

if __name__ == "__main__":
    build_and_push(sys.argv[1], sys.argv[2], sys.argv[3])
