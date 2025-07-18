
# Pipeline 1 – Build Pipeline (MarketMap)

## Purpose
This pipeline is responsible for building the **Services, SQL, and Metadata components** of the MarketMap backend project. It:
- Builds JAR files based on selected components.
- Organizes builds into `Builds/<RELEASE>` folders.
- Maintains a **CombinedBuild** folder with only the **latest builds** for easy deployment.
- Generates a **manifest file** with the latest build information.

---

## Folder Structure
```
<workspace>/
└── Builds/
    └── <RELEASE>/                # e.g., 25.1.0
        ├── backend-webapi.25.1.0.1807.32.jar
        ├── sql-service.25.1.0.1807.33.jar
        ├── metadata-service.25.1.0.1807.32.jar
        └── CombinedBuild/
            ├── backend-webapi.25.1.0.1807.32.jar
            ├── sql-service.25.1.0.1807.33.jar
            ├── metadata-service.25.1.0.1807.32.jar
            └── build_manifest.txt
```

---

## Input Parameters
- **`BUILD_SERVICES`** (boolean): Build Services component.
- **`BUILD_SQL`** (boolean): Build SQL component.
- **`BUILD_METADATA`** (boolean): Build Metadata component.
- **`RELEASE`** (string): Release version (e.g., `25.1.0`).

---

## Stages

### 1. Checkout Code
- Fetches the code from the current Git branch.

### 2. Prepare Folders
- Creates `Builds/<RELEASE>` and `Builds/<RELEASE>/CombinedBuild` if they do not exist.

### 3. Build Components
- **For each selected component:**
  - Runs `mvn clean package` to create JAR.
  - Renames it to:  
    ```
    <component>.<RELEASE>.<ddMM>.<BUILD_NUMBER>.jar
    ```
  - Moves it to `Builds/<RELEASE>`.
  - Removes any old JAR for that component from `CombinedBuild` and copies the new JAR there.

### 4. Update Combined Manifest
- Deletes old `build_manifest.txt`.
- Creates a new manifest with:
  - Release number.
  - Timestamp.
  - Latest JAR names.

### 5. Summary of Combined Build
- Prints `build_manifest.txt` contents in Jenkins console.

### 6. Archive Artifacts
- Archives both `Builds/<RELEASE>` and `CombinedBuild` folders.

---

## Sample Manifest File
```
# Build Manifest for RELEASE 25.1.0
# Last Updated: Fri 07/18/2025 18:10:12
backend-webapi.25.1.0.1807.32.jar
sql-service.25.1.0.1807.33.jar
metadata-service.25.1.0.1807.32.jar
```

---

## Key Features
- **Incremental Builds:** Developers can build individual components.
- **Latest Build Tracking:** CombinedBuild always has the latest versions.
- **Deployment Ready:** UAT/Prod deployments can directly use `CombinedBuild`.

---

## Next Steps
- **Pipeline 2:** Docker packaging and pushing JARs from `CombinedBuild`.
- **Pipeline 3:** Environment setup (EC2/Ansible).
- **Pipeline 4:** Deployment of containers to environments.
