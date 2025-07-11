import os
import subprocess
import shutil
import sys

# STEP 1: Read ENV variables
component = os.getenv("COMPONENT", "ALL")
client = os.getenv("CLIENT", "DefaultClient")
environment = os.getenv("ENVIRONMENT", "DEV")
workspace = os.getenv("WORKSPACE", os.getcwd())
maven_path = r"C:\ProgramData\Jenkins\.jenkins\tools\hudson.tasks.Maven_MavenInstallation\Maven\bin\mvn.cmd"

# STEP 2: Map COMPONENT to actual Maven module(s)
component_map = {
    "Services": "backend-webapi",
    "SQL": "sql-service",
    "Metadata": "metadata-service",
    "ALL": "backend-webapi,sql-service,metadata-service"
}
mapped_modules = component_map.get(component, "")
if not mapped_modules:
    print(f"[ERROR] Invalid COMPONENT: {component}")
    sys.exit(1)

print(f"Selected COMPONENT: {component}")
print(f"Mapped Maven Module(s): {mapped_modules}")

# STEP 3: Run Maven Build
try:
    mvn_cmd = [maven_path, "clean", "install", "-pl", mapped_modules, "-am"]
    result = subprocess.run(mvn_cmd, cwd=workspace, check=True)
    print("Maven build successful")
except subprocess.CalledProcessError:
    print("Maven build failed")
    sys.exit(1)

# STEP 4: Deploy Artifacts
deploy_path = os.path.join(workspace, "deploy", client, environment)
os.makedirs(deploy_path, exist_ok=True)

paths = {
    "backend-webapi": "Services",
    "sql-service": "SQL",
    "metadata-service": "Metadata"
}

print(f"\nDeploying to folder: {deploy_path}")

for module_dir, comp_key in paths.items():
    if component == "ALL" or component == comp_key:
        target_dir = os.path.join(workspace, module_dir, "target")
        deploy_dir = os.path.join(deploy_path, module_dir.split("-")[0])
        os.makedirs(deploy_dir, exist_ok=True)

        # Clean old files
        for f in os.listdir(deploy_dir):
            try:
                os.remove(os.path.join(deploy_dir, f))
            except Exception as e:
                print(f"Error removing {f}: {e}")

        # Copy .jar from target
        jar_files = [f for f in os.listdir(target_dir) if f.endswith(".jar")]
        if not jar_files:
            print(f"[WARN] No .jar found in {target_dir}")
        for jar in jar_files:
            src = os.path.join(target_dir, jar)
            dest = os.path.join(deploy_dir, jar)
            shutil.copy2(src, dest)
            print(f"✔ Copied: {src} → {dest}")

print("Deployment complete.")
sys.exit(0)