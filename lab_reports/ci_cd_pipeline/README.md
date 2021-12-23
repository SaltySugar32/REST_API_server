## CI/CD pipeline Report

---

### Workflow build_app
- Runs on commit.
- Installs all dependencies.
![](build_dependencies.png)
- Uses Flake8 and black tools
![](build_tools.png)
- Runs unit tests
![](build_tests.png)

### Workflow deploy_dev
- Runs on demand.
- Deploys dev environment to server via SSH
![](deploy_dev.png)

### Workflow deploy_prod
- Runs on demand.
- Deploys prod environment to server via SSH
![](deploy_prod.png)