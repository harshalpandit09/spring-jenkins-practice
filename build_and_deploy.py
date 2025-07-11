import os
import shutil

# Read environment variables
component = os.environ.get('COMPONENT', 'ALL')
client = os.environ.get('CLIENT', 'DefaultClient')
env = os.environ.get('ENVIRONMENT', 'DEV')
workspace = os.environ.get('WORKSPACE', os.getcwd())

component_map = {
    'Services': 'backend-webapi',
    'SQL': 'sql-service',
    'Metadata': 'metadata-service',
    'ALL': ['backend-webapi', 'sql-service', 'metadata-service']
}

if component == 'ALL':
    selected_modules = component_map['ALL']
else:
    selected_modules = [component_map.get(component)]

deploy_path = os.path.join(workspace, 'deploy', client, env)

for module in ['backend-webapi', 'sql', 'metadata']:
    path = os.path.join(deploy_path, module)
    os.makedirs(path, exist_ok=True)
    # Clean directory
    for f in os.listdir(path):
        try:
            os.remove(os.path.join(path, f))
        except Exception:
            pass

for module in selected_modules:
    source_jar = os.path.join(workspace, module, 'target')
    target_subfolder = module.split('-')[0] if '-' in module else module
    target_path = os.path.join(deploy_path, target_subfolder)
    if os.path.exists(source_jar):
        for file in os.listdir(source_jar):
            if file.endswith('.jar'):
                shutil.copy2(os.path.join(source_jar, file), target_path)
