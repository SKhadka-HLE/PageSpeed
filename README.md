
# 📊 page speed
Some tool that does something

## 🚀 Quick Summary
TODO:  Lance add something here

### 🧱 First-Time Setup
Fork the repository

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd PageSpeed
```

### 2. Install Required Versions
TODO: Lance
```bash
	# Python
	# Ensure Python 3.9.x is installed
		python3.9 --version
		pyenv install 3.9.13 (using pyenv)
		pyenv local 3.9.13
```

### 3. Setup Environment
```bash
	# Run this script to automatically configure environment, which will:
		# 	Activate correct Node version from .nvmrc
		# 	Create a virtual environment .venv (if not present)
		# 	Activate .venv
	source env_setup.sh
```

### 4. Install Dependencies
```bash
	# Python
		pip install -r requirements.txt
	# Node.js (Serverless plugins)
		yarn install
```

### 5. Run locally
```bash
	# Use the helper script:
			source run_local.sh
	# Manually
			source .venv/bin/activate
			sls offline
```

### 🧠 Tips and Best Practices
	Use .nvmrc and .env to keep environments consistent.
	Always run source env_setup.sh before local dev or deployment.

"# PageSpeed"
This proejct collects PagspEeed metrics data
