# 🤝 Contributing to AquaTrace

Thank you for your interest in contributing to AquaTrace! We're excited to have you join our mission to monitor and improve global water quality.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [Areas for Contribution](#areas-for-contribution)

## 📜 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or experience level.

### Expected Behavior
- Be respectful and professional
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other contributors

## 🚀 How to Contribute

### Reporting Bugs 🐛

Found a bug? Please create an issue with:
- **Clear title**: Brief description of the issue
- **Description**: Detailed explanation of the problem
- **Steps to reproduce**: 
  1. Step one
  2. Step two
  3. etc.
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Environment**:
  - OS: (e.g., Windows 11, Ubuntu 22.04)
  - Python version: (e.g., 3.13)
  - Node.js version: (e.g., 18.17)
  - Browser: (e.g., Chrome 120)

### Suggesting Features 💡

Have an idea? Create an issue with:
- **Feature description**: Clear explanation of the feature
- **Use case**: Why this feature is needed
- **Benefits**: How it improves the project
- **Implementation ideas**: Suggested approach (optional)
- **Mockups/Examples**: Visual representation (optional)

### Asking Questions ❓

- Check existing documentation and issues first
- Use [GitHub Discussions](https://github.com/yourusername/aquatrace/discussions) for questions
- Be specific and provide context

## 🛠️ Development Setup

### Prerequisites
- Python 3.13+
- Node.js 16+
- Git
- Virtual environment tool

### Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/aquatrace.git
cd aquatrace

# Add upstream remote
git remote add upstream https://github.com/original/aquatrace.git
```

### Backend Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy geoalchemy2 xarray tensorflow

# Run backend
cd backend
uvicorn api.main:app --reload
```

### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Verify Setup
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## 📝 Coding Standards

### Python (Backend)

#### Style Guide
- Follow **PEP 8**
- Use **type hints** for function parameters and returns
- Maximum line length: **88 characters** (Black formatter)
- Use **docstrings** for all functions and classes

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🔄 Pull Request Process

1. **Fork** the repository
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** following coding standards
4. **Write tests** for new features
5. **Ensure tests pass**
6. **Commit**: `git commit -m 'feat: add amazing feature'`

### JavaScript/React
- Use ES6+ features
- Follow Airbnb style guide
- Use functional components with hooks
- PropTypes for all components

## Documentation

- Update README.md if you change functionality
- Document all new functions and classes
- Update API documentation for endpoint changes
- Add comments for complex logic

## Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and PRs when applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions or concerns!
