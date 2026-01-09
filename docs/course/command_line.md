# Command Line Guide

Source: https://skaftenicki.github.io/dtu_mlops/s1_development_environment/command_line/

## Core Concepts

The command line provides a text-based interface essential for MLOps work, especially for cloud environments and tools lacking graphical interfaces.

### Anatomy of Commands

Commands follow this structure:

1. **Prompt**: Shows current directory and environment (e.g., `$`, `>`, `:`)
2. **Command**: The executable (e.g., `ls`, `cd`)
3. **Options/Flags**: Modify behavior, prefixed with `-` or `--` (e.g., `-l`)
4. **Arguments**: Specify what the command operates on

Example: `ls -l figures`
- Command: `ls`
- Option: `-l`
- Argument: `figures`

## Essential Commands

| Command | Purpose |
|---------|---------|
| `cd` | Navigate between directories |
| `pwd` | Display current directory |
| `ls` | List folder contents (`-l` for detailed view) |
| `which` | Locate command executables |
| `echo` | Print text |
| `cat` | Display file contents |
| `wget` | Download files |
| `less` | View files page-by-page |
| `top` | Monitor system processes |
| `nano` | Text editor |

## Key Features & Tips

- **Tab completion**: Autocompletes commands and filenames
- **Output redirection**: Use `>` to redirect output to files
- **Environment variables**: Store dynamic values using `export VAR=value` (Linux/Mac) or `set VAR=value` (Windows)
- **`.env` files**: Store multiple environment variables; load with `python-dotenv` package

## Scripting Basics

**Bash script structure**:
```bash
#!/bin/bash
# Script body
echo Hello World!
```

Access environment variables in Python via `os.environ["VAR_NAME"]`.

## Important Flags

- `-h` or `--help`: Displays command help and options
- `-V` or `--version`: Shows installed program version

## Platform Notes

Windows users should use **Windows Subsystem for Linux (WSL)** for full bash support and consistent command compatibility.
