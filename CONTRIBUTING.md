# Contributing to Stress Tests

Thank you for your interest in contributing to the Stress Tests project! This document provides guidelines for contributors.

## Getting Started

### Prerequisites

- Linux operating system
- Just command runner (`cargo install just` or `sudo apt install just`)
- Git
- Python 3.8+

### Initial Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/stress-tests.git
   cd stress-tests
   ```

3. Set up your development environment:
   ```bash
   just setup
   ```

4. Run the full test suite to ensure everything works:
   ```bash
   just full_test
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them:
   ```bash
   just full_test
   ```

3. Review the generated report to verify your changes work as expected.

### Code Style

#### Python

- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep lines under 88 characters

#### Shell Scripts

- Use `#!/bin/bash` shebang
- Use `set -euo pipefail` for safety
- Add comments explaining complex operations
- Quote variables properly

#### Justfile

- Keep commands organized and readable
- Use meaningful recipe names
- Add comments explaining complex recipes

### Testing

Before submitting your contribution, ensure:

1. All tests pass with your changes
2. The report generates correctly
3. Plots display properly
4. No new errors appear in the logs

### Submitting Changes

1. Commit your changes with a descriptive message following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary):
   ```bash
   git commit -m "feat: brief description of changes"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a pull request with:
   - Clear title and description
   - Screenshots if applicable
   - Steps to reproduce any fixes

## Types of Contributions

We welcome several types of contributions:

### Bug Fixes

- Fix errors in existing functionality
- Improve error handling
- Resolve edge cases

### New Features

- Add new stress tests
- Enhance reporting capabilities
- Add support for new hardware

### Documentation

- Improve README documentation
- Add inline code comments
- Update examples

### Code Quality

- Refactor existing code
- Improve performance
- Add test coverage

## Areas for Contribution

### High Priority

1. **New Stress Tests**
   - Network stress testing
   - Disk I/O stress testing
   - Mixed workload tests

2. **Enhanced Reporting**
   - PDF report generation
   - Comparison views between runs
   - Performance recommendations

3. **Platform Support**
   - macOS support
   - Windows support
   - Container support

### Medium Priority

1. **User Interface**
   - CLI progress bars
   - Interactive configuration
   - Real-time monitoring

2. **Advanced Features**
   - Scheduled testing
   - Historical data storage
   - Baseline comparison

## Review Process

All contributions go through a review process:

1. Initial automated checks
2. Code review by maintainers
3. Testing on multiple systems
4. Merge if approved

## Getting Help

If you need help with your contribution:

1. Check existing issues and discussions
2. Create a new issue with your question
3. Include relevant code and error messages
4. Describe your system environment

## Recognition

Contributors are recognized in the project through:

- Attribution in commit messages
- Inclusion in AUTHORS file
- Recognition in release notes
- Invitation to become maintainers

Thank you for contributing to the Stress Tests project!
