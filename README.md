# Azure Machine Learning Playground

A structured repository for learning and experimenting with Azure Machine Learning. From local development in GitHub Codespaces to cloud-based ML workflow orchestration.

## Overview

This project demonstrates professional ML workflows with Azure ML:
- **Notebooks** for interactive development and job orchestration
- **Python scripts** for reproducible training on Azure ML Compute
- **Git-based workflow** instead of Azure ML Studio UI
- **GitHub Codespaces** as development environment

## Repository Structure

```
azure-machine-learning-playground/
├── .devcontainer/          # Codespaces configuration
│   └── devcontainer.json   # Python 3.11 + Azure CLI + Extensions
├── notebooks/              # Jupyter Notebooks for development
│   ├── 00_setup_connection.ipynb    # Connect to Azure ML Workspace
│   └── 01_iris_training.ipynb       # Example: Iris dataset training
├── src/                    # Python scripts for Azure ML jobs
│   ├── __init__.py
│   └── train.py            # Training script (runs on Azure ML)
├── configs/                # Configuration files
│   └── .gitkeep
├── .gitignore              # Python, Jupyter, Azure ML ignores
├── .gitattributes          # nbstripout for notebooks
├── requirements.txt        # Azure ML SDK + dependencies
└── README.md               # This file
```

## Prerequisites

### Azure Resources
- **Azure Subscription** (Free Trial or paid)
- **Azure ML Workspace** created (can also be done in first notebook)

### Local Environment
- **GitHub Account** (GitHub Pro recommended for private repos)
- **GitHub Codespaces** enabled

## Setup

### 1. Open Repository in Codespaces

1. Open this repository on GitHub
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for Codespaces to load (approx. 2-3 minutes on first launch)

The `devcontainer.json` automatically installs:
- Python 3.11
- Azure CLI
- All Python dependencies from `requirements.txt`
- Jupyter extensions
- nbstripout for Git

### 2. Set up Azure Authentication

In Codespaces terminal:

```bash
# Azure CLI Login
az login --use-device-code

# Set subscription (if multiple available)
az account list --output table
az account set --subscription "<Your-Subscription-ID>"
```

### 3. Create Azure ML Workspace (if not already exists)

**Option A: Via Azure Portal**
1. Go to portal.azure.com
2. Create Resource Group (e.g., `rg-ml-playground`)
3. Create Azure ML Workspace (e.g., `mlw-playground`)

**Option B: Via Azure CLI (in Codespaces terminal)**
```bash
# Create Resource Group
az group create --name rg-ml-playground --location westeurope

# Create Azure ML Workspace
az ml workspace create \
  --name mlw-playground \
  --resource-group rg-ml-playground \
  --location westeurope
```

### 4. Open First Notebook

Open `notebooks/00_setup_connection.ipynb` and follow instructions to:
- Connect to your Azure ML Workspace
- Create a compute cluster
- Test the connection

## Workflow

### Local Development → Azure ML Execution

```
Codespaces (local)
  ↓
Write/execute notebook
  ↓
Define Azure ML job (command)
  ↓
Submit job to Azure ML
  ↓
Azure ML Compute executes src/train.py
  ↓
View results in Azure ML Studio
```

### Typical Steps

1. **Experiment** in notebooks (locally in Codespaces)
2. **Extract training code** to `src/train.py`
3. **Define job** in notebook using `azure.ai.ml.command()`
4. **Start job** with `ml_client.jobs.create_or_update()`
5. **Monitor** in Azure ML Studio or via SDK
6. **Register and deploy** model

## Important Concepts

### Where Does What Run?

- **Notebooks**: Run in Codespaces (local, free with GitHub Pro)
- **Training scripts**: Run on Azure ML Compute (paid, only during job)
- **Data**: Stored in Azure Blob Storage or Azure ML Datastores
- **Models**: Stored in Azure ML Model Registry

### Git Best Practices

- **Data**: NOT in Git → Azure Blob Storage
- **Models**: NOT in Git → Azure ML Model Registry
- **Code**: YES in Git → src/, notebooks/
- **Notebooks**: With nbstripout (output automatically removed)

## Cost Awareness

### Free
- GitHub Codespaces (60 hours/month with Pro, 120 core hours)
- Azure ML Workspace (only metadata)

### Paid
- Azure ML Compute (only when jobs run!)
- Azure Blob Storage (very cheap)
- Deployed models (if deployed)

**Tip**: Configure compute cluster with `min_instances=0` → scales to 0 when not in use!

## Next Steps

1. ✅ Complete setup (`00_setup_connection.ipynb`)
2. ✅ Run first training (`01_iris_training.ipynb`)
3. 📚 Add more examples (your own code!)
4. 🚀 Try your own datasets and models

## Resources

- [Azure ML Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/)
- [Azure ML Python SDK v2](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-ml-readme)
- [Azure ML Examples (Microsoft)](https://github.com/Azure/azureml-examples)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)

## Troubleshooting

### "Authentication failed"
```bash
# Re-login
az login --use-device-code
az account set --subscription "<Your-Subscription-ID>"
```

### "Compute cluster not found"
Create a compute cluster in the notebook or via CLI:
```bash
az ml compute create --name cpu-cluster --type amlcompute --min-instances 0 --max-instances 4
```

### Notebook kernel doesn't start
```bash
# In terminal
pip install --upgrade ipykernel
```

## License

This project is for educational purposes.
