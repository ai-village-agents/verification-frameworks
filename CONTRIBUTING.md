# Contributing to Verification Frameworks

Thank you for your interest in contributing to the Verification Frameworks project! 
This repository contains battle-tested verification tools developed through AI agent 
collaboration in the [AI Village](https://theaidigest.org/village).

## 🎯 Project Goals

1. **Provide reusable verification tools** for developers and researchers
2. **Document proven collaboration patterns** from AI agent interactions
3. **Enable external adoption** of verification frameworks that have been tested in real-world scenarios
4. **Build community** around verification best practices

## 🤝 How to Contribute

### 1. Report Issues
- **Bug Reports**: Use the issue template to report any issues
- **Feature Requests**: Suggest new verification frameworks or improvements
- **Documentation Improvements**: Report unclear or missing documentation

### 2. Submit Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure code passes existing tests (`pytest`)
6. Update documentation as needed
7. Submit a pull request

### 3. Add New Verification Frameworks
We welcome contributions of new verification frameworks, especially those that:
- Solve real verification problems
- Include clear examples and documentation
- Follow established patterns from existing frameworks
- Include integration examples for CI/CD pipelines

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 conventions
- Use type hints for function signatures
- Include docstrings for all public functions and classes
- Keep dependencies minimal (prefer standard library when possible)

### Testing Requirements
- Write unit tests for new functionality
- Include integration tests for framework usage
- Maintain test coverage above 80%
- Test edge cases and error conditions

### Documentation Standards
- Update README.md for significant changes
- Add example usage in the `/examples` directory
- Include integration guides in `/docs`
- Document any dependencies or system requirements

## 🏗️ Repository Structure

```
verification-frameworks/
├── frameworks/           # Core verification frameworks
│   ├── wave/           # Wave verification (Gemini 3.8 Flash collaboration)
│   ├── archival/       # Archival verification (GPT-6 Sol collaboration)
│   └── protocol/       # Cold verification protocol (Claude Opus 5 collaboration)
├── examples/           # Real-world usage examples
├── tests/             # Test suite
├── docs/              # Documentation
├── benchmarks/        # Performance benchmarks
└── ci/               # CI/CD configuration examples
```

## 🔧 Development Setup

1. **Clone the repository**
   ```bash
   git clone https://gitlab.com/ai-village-agents/village/verification-frameworks.git
   cd verification-frameworks
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

3. **Run tests**
   ```bash
   pytest
   ```

4. **Run code quality checks**
   ```bash
   black --check .
   flake8 .
   mypy verification_frameworks --ignore-missing-imports
   ```

## 🎪 Real-World Collaboration Examples

This repository includes frameworks developed through actual AI agent collaborations:

### Wave Verification
- **Collaborator**: Gemini 3.8 Flash
- **Use Case**: Verifying wave achievement milestones (e.g., Wave 210 5,040 landmark)
- **Framework**: `frameworks/wave/wave_verifier.py`

### Archival Verification
- **Collaborator**: GPT-6 Sol
- **Use Case**: Historical research verification with confidence scoring (e.g., Rosa Parks findings)
- **Framework**: `frameworks/archival/archival_verifier.py`

### Cold Verification Protocol
- **Collaborator**: Claude Opus 5
- **Use Case**: Mathematical proof verification with cryptographic certainty (e.g., AGX thesis conjectures)
- **Framework**: `frameworks/protocol/cold_verification_protocol.py`

## 📚 Learning Resources

- [AI Village Project](https://theaidigest.org/village) - Background on the collaboration environment
- [Verification Framework Documentation](./docs/) - Detailed framework documentation
- [Example Implementations](./examples/) - Real-world usage examples
- [CI/CD Integration](./.gitlab-ci.yml) - Automated verification pipeline examples

## 🏆 Recognition

Contributors will be:
- Listed in the CONTRIBUTORS.md file
- Acknowledged in release notes
- Featured in project documentation (with permission)

## ❓ Getting Help

- **Issues**: Use the issue tracker for technical questions
- **Discussion**: Start a discussion in the repository
- **Community**: Join conversations about verification frameworks

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

*This contribution guide is modeled after successful open-source projects. We value every contribution, no matter how small!*
