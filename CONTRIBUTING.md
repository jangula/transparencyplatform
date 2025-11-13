# Contributing to National Strategy Transparency Platform

Thank you for your interest in contributing to the National Strategy Transparency Platform! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, browser, etc.)

### Suggesting Features

Feature suggestions are welcome! Please include:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach
- Mockups or examples if applicable

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/transparency-platform.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments where necessary
   - Update documentation

4. **Test your changes**
   - Run existing tests
   - Add new tests for new features
   - Ensure all tests pass

5. **Commit your changes**
   ```bash
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**
   - Provide clear description
   - Reference any related issues
   - Wait for review

## 📝 Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions/classes
- Keep functions focused and small
- Use meaningful variable names

### TypeScript/React (Frontend)
- Use functional components with hooks
- Follow React best practices
- Use TypeScript strictly (no `any` types)
- Keep components small and reusable
- Use meaningful prop names

### Commit Messages
Follow conventional commits format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Example:
```
feat: Add question filtering by date range
fix: Resolve null pointer in strategy detail page
docs: Update README with new features
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📋 Pull Request Checklist

Before submitting a PR, ensure:
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description is complete

## 🔍 Code Review Process

1. PR is submitted
2. Automated tests run
3. Code review by maintainers
4. Address feedback if needed
5. Approval and merge

## 🌟 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Project documentation

## 📞 Getting Help

- Open an issue for questions
- Join discussions in GitHub Discussions
- Check existing documentation

## 🚫 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professional communication

Thank you for contributing to Namibia's digital transparency! 🇳🇦
