---
name: "readme-generator"
description: "Generates comprehensive project documentation including README.md, architecture docs, and API docs. Invoke when user asks to create, update, or generate project documentation."
---

# README Generator

This skill helps generate comprehensive project documentation automatically.

## When to Invoke

Invoke this skill when:
- User asks to "generate README"
- User asks to "create project documentation"
- User asks to "update README.md"
- User mentions "project documentation" or "docs"
- User wants to document a new project or feature

## What It Does

1. **Analyzes Project Structure**
   - Scans project directory structure
   - Identifies main components and modules
   - Detects technology stack (languages, frameworks, dependencies)

2. **Generates Documentation**
   - Creates comprehensive README.md
   - Includes project overview, features, installation, usage
   - Adds architecture diagrams if applicable
   - Documents API endpoints and configuration

3. **Updates Existing Docs**
   - Updates outdated documentation
   - Maintains consistency across docs
   - Preserves custom sections

## Documentation Structure

### README.md Template

```markdown
# Project Name

Brief description of the project.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
# Installation commands
\`\`\`

## Quick Start

\`\`\`bash
# Quick start commands
\`\`\`

## Usage

Basic usage examples.

## Architecture

Project architecture overview.

## API Reference

API documentation (if applicable).

## Configuration

Configuration options.

## Contributing

Contribution guidelines.

## License

License information.
```

## Process

1. **Scan Project**
   - Read package.json, requirements.txt, or similar
   - Analyze directory structure
   - Identify main entry points

2. **Extract Information**
   - Project name and description
   - Dependencies and versions
   - Scripts and commands
   - Configuration files

3. **Generate Documentation**
   - Create structured README.md
   - Add relevant sections
   - Include code examples
   - Add badges and links

4. **Review and Refine**
   - Check for completeness
   - Verify accuracy
   - Add missing sections

## Examples

### Example 1: New Project

User: "Generate README for this project"

Action:
1. Scan project structure
2. Identify Python project with requirements.txt
3. Generate comprehensive README.md
4. Include installation, usage, and API docs

### Example 2: Update Existing

User: "Update the README"

Action:
1. Read existing README.md
2. Scan for changes in project
3. Update outdated sections
4. Preserve custom content

## Best Practices

1. **Keep it Simple**
   - Clear, concise language
   - Avoid jargon
   - Use examples

2. **Be Comprehensive**
   - Cover all important aspects
   - Include troubleshooting
   - Add FAQ section

3. **Maintain Consistency**
   - Use consistent formatting
   - Follow documentation standards
   - Keep sections organized

4. **Update Regularly**
   - Keep docs in sync with code
   - Update after major changes
   - Review periodically

## Output

The skill will generate:
- `README.md` - Main project documentation
- Optional: `docs/` directory with additional docs
- Optional: `CHANGELOG.md` if requested
- Optional: `CONTRIBUTING.md` if requested

## Notes

- Always verify generated content
- Customize for specific project needs
- Keep documentation up-to-date
- Consider target audience
