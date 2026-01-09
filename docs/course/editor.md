# Editor/IDE Guide

Source: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/editor/

## Recommended Editors

| Editor | Key Characteristic |
|--------|-------------------|
| **Spyder** | MATLAB-like environment, beginner-friendly |
| **Visual Studio Code** | Multi-language support, easy setup |
| **PyCharm** | Professional Python IDE, steeper learning curve |

**Primary recommendation:** Visual Studio Code for those without an existing setup.

## VS Code Essential Extensions for Python/ML

1. **Python** — Core Python language support
2. **Pylance** — Language server enabling improved code completion and type-checking
3. **Jupyter** — Native notebook support within the editor
4. **Python Environments** — Virtual environment management interface

## Key VS Code Components

- **Action bar**: Navigate between installed extensions and tools
- **Sidebar**: File explorer and extension-specific views
- **Editor**: Code workspace supporting multiple column layouts
- **Panel**: Integrated terminal for script execution and environment management
- **Status bar**: Environment selection and extension information

## GitHub Copilot for AI-Assisted Development

**Setup**: Free for students via the Student Developer Pack; install the GitHub Copilot extension.

**Primary features**:
- Real-time code completion suggestions based on current context
- Inline code generation (press `Ctrl+i` to open chat)
- Terminal error explanation via command palette

## ML Development Best Practices

- Use `.py` scripts rather than notebooks for production workflows
- Convert notebooks to scripts using `nbconvert` when deploying models
- Critically evaluate all AI-generated suggestions before implementation
- Leverage editor context-awareness to reduce productivity loss from switching between tools

## Useful Keyboard Shortcuts (VS Code)

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Command palette |
| `Ctrl+P` | Quick file open |
| `F5` | Start debugging |
| `F9` | Toggle breakpoint |
| `Ctrl+`` ` | Toggle terminal |
| `Ctrl+i` | Open Copilot chat |
