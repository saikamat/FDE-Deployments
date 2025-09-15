# FDE-Deployments

This repository contains deployment scripts and applications for FDE (Full Data Engineering) projects.

## Repository Structure

```
FDE-Deployments/
├── 01-cursor-generated-chatbot/    # Streamlit chatbot powered by Amazon Bedrock
│   ├── app.py                      # Main application file
│   ├── requirements.txt            # Python dependencies
│   ├── docs/                       # Documentation (see docs branch)
│   └── tests/                      # Test files
├── .gitignore                      # Git ignore rules for sensitive data
└── README.md                       # This file
```

## Branch Structure

This repository uses a multi-branch approach to organize different types of content:

### Main Branch (`main`)
- Contains the core application code
- Sensitive data (CSV files, .env files) are protected by `.gitignore`
- Focused on production-ready code

### Documentation Branch (`docs`)
- Contains all documentation files
- Includes comprehensive guides for architecture, authentication, styling, etc.
- Separate from main codebase to keep main branch clean

## Getting Started

### Working with Code (Main Branch)
```bash
# Switch to main branch
git checkout main

# Your docs/ folder will be ignored here
# Work on your application code
git add .
git commit -m "Update application code"
```

### Working with Documentation (Docs Branch)
```bash
# Switch to docs branch
git checkout docs

# Make changes to docs/
git add .
git commit -m "Update documentation"
```

### Pushing to GitHub
```bash
# Push main branch
git push origin main

# Push docs branch
git push origin docs
```

## Security Features

### Protected Sensitive Data
The following file types are automatically ignored by git:
- `*.csv` - CSV files (contains AWS credentials)
- `.env` - Environment variable files
- `*.pem` - Private key files
- `*.key` - Cryptographic key files

### Branch Isolation
- **Main branch**: Code only, no documentation clutter
- **Docs branch**: Documentation only, separate from codebase
- Sensitive data remains protected on both branches

## Projects

### 01-cursor-generated-chatbot
A Streamlit-based question-answering chatbot powered by Amazon Bedrock's Claude Sonnet model.

**Quick Start:**
```bash
cd 01-cursor-generated-chatbot
pip install -r requirements.txt
streamlit run app.py
```

For detailed setup instructions, see the [chatbot README](01-cursor-generated-chatbot/README.md).

## Contributing

1. **For Code Changes**: Work on the `main` branch
2. **For Documentation**: Work on the `docs` branch
3. **Never commit sensitive data**: CSV files, .env files, and keys are automatically ignored
4. **Use descriptive commit messages**: Clearly describe what you're changing

## Branch Management

### Creating New Branches
```bash
# Create feature branch from main
git checkout main
git checkout -b feature/new-feature

# Create documentation branch
git checkout docs
git checkout -b docs/new-docs
```

### Merging Changes
```bash
# Merge feature into main
git checkout main
git merge feature/new-feature

# Merge docs updates
git checkout docs
git merge docs/new-docs
```

## Best Practices

- ✅ Keep sensitive data out of version control
- ✅ Use separate branches for different content types
- ✅ Write clear commit messages
- ✅ Test changes before committing
- ❌ Never commit credentials or API keys
- ❌ Don't mix documentation with code in main branch

## Support

For issues related to:
- **Application code**: Check the main branch and project-specific READMEs
- **Documentation**: Check the docs branch
- **Security concerns**: Review `.gitignore` and branch structure
