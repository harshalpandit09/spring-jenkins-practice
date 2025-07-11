import os
import shutil
import subprocess
import sys

# STEP 1: Map Jenkins parameter COMPONENT to actual Maven module names
def map_component_to_module(component):
    return {
        "Services": "backend-webapi",           # Maps "Services" to the Spring Boot API module
        "SQL": "sql-service",                   # Maps "SQL" to the SQL scripts module
        "Metadata": "metadata-service",         # Maps "Metadata" to the metadata module
        "ALL": "backend-webapi,sql-service,metadata-service"  # Builds everything
    }.get(component, "")  # Return empty string if no match found

# STEP 2: Run Maven build for selected modules
def run_maven_build(component):
    module = map_component_to_module(component)

    if not module:
        print(f"Invalid COMPONENT: {component}")
        sys.exit(1)

    print(f"🔧 Running Maven build for: {module}")

    # Runs: mvn clean install -pl module -am
    result = subprocess.run(
        ["mvn", "clean", "install", "-pl", module, "-am"],
        shell=True
    )

    if result.returncode != 0:
        print("Maven build failed.")
        sys.exit(result.returncode)

# STEP 3: Clean existing deploy folders and create structure again
def clean_and_prepare_deploy_folders(deploy_path):
    # For each module, clean the folder if exists or create new
    for folder in ["backend-webapi", "sql", "metadata"]:
        full_path = os.path.join(deploy_path, folder)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)  # Delete old files
        os.makedirs(full_path)        # Create fresh folder

    print(f"Cleaned and created deploy folders under: {deploy_path}")

# STEP 4: Copy final JAR files into the appropriate deploy folders
def copy_artifacts(component, workspace, deploy_path):
    # Map component to its corresponding folder name
    module_map = {
        "Services": "backend-webapi",
        "SQL": "sql-service",
        "Metadata": "metadata-service"
    }

    print("Copying build outputs...")

    # If ALL is selected, copy all modules
    selected = ["Services", "SQL", "Metadata"] if component == "ALL" else [component]

    for comp in selected:
        module_dir = module_map.get(comp)
        if not module_dir:
            continue

        # Source: build output from Maven
        src_dir = os.path.join(workspace, module_dir, "target")

        # Target: deploy location (folder differs slightly)
        tgt_dir = os.path.join(deploy_path, module_dir if comp == "Services" else comp.lower())

        os.makedirs(tgt_dir, exist_ok=True)

        # Copy only .jar files to deploy folder
        for file in os.listdir(src_dir):
            if file.endswith(".jar"):
                shutil.copy(os.path.join(src_dir, file), tgt_dir)
                print(f"Copied {file} → {tgt_dir}")

# MAIN ENTRY: Called when script runs
def main():
    # STEP 0: Read Jenkins parameters (set from Build With Parameters)
    component = os.environ.get("COMPONENT", "ALL")
    environment = os.environ.get("ENVIRONMENT", "DEV")
    client = os.environ.get("CLIENT", "HSBC")

    # Get Jenkins workspace path
    workspace = os.getcwd()

    # Construct dynamic path: deploy/CLIENT/ENVIRONMENT/
    deploy_path = os.path.join(workspace, "deploy", client, environment)

    # Run pipeline steps
    run_maven_build(component)
    clean_and_prepare_deploy_folders(deploy_path)
    copy_artifacts(component, workspace, deploy_path)

    print("Build and deployment complete!")

# Standard Python entry point
if __name__ == "__main__":
    main()