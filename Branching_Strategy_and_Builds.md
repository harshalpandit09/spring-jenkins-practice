
# Branching and Build Strategy Documentation

## 1. Branching Strategy

### Purpose
Our Jenkins Multibranch Pipeline is set up to build **separate workspaces and artifacts** for each branch.  
This ensures that builds for `main`, `release/*`, or `feature/*` branches remain isolated.

### Branch Types
- **main:** Always points to the latest development version (e.g., 25.2.0).
- **release/*:** Represents stable releases, e.g., `release/25.1.0`.
- **feature/*:** Represents feature-specific development branches.

---

## 2. Creating a New Branch

### Option 1: From GitHub UI
1. Go to the repository:  
   `https://github.com/harshalpandit09/spring-jenkins-practice`  
2. Click on the **branch dropdown** (next to `main`).  
3. Enter the new branch name (e.g., `release/25.2.0`).  
4. Click **“Create branch: release/25.2.0 from main”**.

### Option 2: From Command Line
```bash
git checkout main
git pull origin main
git checkout -b release/25.2.0
git push origin release/25.2.0
```

---

## 3. Jenkins Behavior for Branches

- Each branch (e.g., `main`, `release/25.1.0`) creates its own workspace under:
  ```
  C:\ProgramData\Jenkins\.jenkins\workspace\MarketMap-MBP_<branch_name>
  ```

- Each branch has its own build artifacts stored under:
  ```
  Builds/<RELEASE>/
  ```

- `CombinedBuild` folder is **branch-specific**.  
  For example:
  - `main` → Builds/25.2.0/CombinedBuild/
  - `release/25.1.0` → Builds/25.1.0/CombinedBuild/

---

## 4. Pipeline Behavior per Branch

1. Developer selects which components to build (Services/SQL/Metadata).  
2. JARs are generated under `Builds/<RELEASE>/`.  
3. `CombinedBuild` is updated with the **latest build** for the selected components.  
4. Manifest file (`build_manifest.txt`) is updated for that branch.  

**Example:**  
```
Builds/25.1.0/
    backend-webapi.25.1.0.1807.32.jar
    sql-service.25.1.0.1807.33.jar
    metadata-service.25.1.0.1807.32.jar
    CombinedBuild/
        backend-webapi.25.1.0.1807.32.jar
        sql-service.25.1.0.1807.33.jar
        metadata-service.25.1.0.1807.32.jar
        build_manifest.txt
```

---

## 5. Deployment Note
Before deploying to UAT/Prod, ensure that **all components** (Services, SQL, Metadata) have been built for that release branch.  
Run a **full build** (all components selected) if needed.

---

## 6. Checklist for Branching Out
1. Create a new branch from `main` (`release/<version>`).  
2. Ensure `Jenkinsfile` is present in the branch.  
3. Go to Jenkins → **MarketMap-MBP** → **Scan Multibranch Pipeline Now**.  
4. Wait for the new branch to appear under the pipeline.  
5. Run **Build with Parameters** on that branch.

---
