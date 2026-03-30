# GitHub File Upload Tool

A simple, powerful bash script to upload any file to a GitHub repository from the terminal. No git commands needed — just point, upload, done.

Supports **Termux**, **Linux**, **macOS**, and **Windows (WSL/Git Bash)**.

---

## Features

- 📤 Upload any file type — txt, pdf, apk, images, archives, binaries, etc.
- 🏗️ Create new repositories on the fly
- 🎯 Works with any GitHub repository (public or private)
- 💾 Saves credentials securely for reuse
- 🔄 Interactive or fully scripted (all flags)
- 🌐 Works on Termux, Linux, macOS, and Windows (WSL/Git Bash)

---

## Requirements

- `git`
- `gh` (GitHub CLI)
- Internet connection

### Install GitHub CLI

**Termux:**
```bash
pkg install gh
```

**Ubuntu/Debian:**
```bash
sudo apt install gh
```

**macOS:**
```bash
brew install gh
```

**Arch Linux:**
```bash
sudo pacman -S github-cli
```

---

## Installation

### Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/papi144/Uplode-tools-to-github-.git
cd Uplode-tools-to-github-

# Make the script executable
chmod +x github-upload

# Move to your PATH (optional)
sudo mv github-upload /usr/local/bin/
```

### Manual Install

1. Clone or download this repository
2. Copy `github-upload` to a folder in your PATH (e.g., `/usr/local/bin/`)
3. Make it executable: `chmod +x github-upload`

---

## Authentication

On first run, the script will prompt for your GitHub credentials:

```bash
./github-upload
```

```
GitHub username: your_username
GitHub Personal Access Token (ghp_...): ghp_your_token_here
```

Your token is saved securely in `~/.config/github-upload/config` (permissions 600).

### Creating a GitHub Token

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Give it the **`repo`** scope
4. Copy the token (starts with `ghp_`)

---

## Usage

### Interactive Mode

```bash
./github-upload
```

The script will guide you step by step.

### Command Line Mode

```bash
# Upload a single file
./github-upload -r user/repo file.txt

# Upload multiple files
./github-upload -r user/repo file1.pdf image.png backup.zip

# Upload with custom commit message
./github-upload -r user/repo -m "Updated logs" logs.txt

# Upload to a specific branch
./github-upload -r user/repo -b develop app.apk

# Create a new repository and upload files
./github-upload -r my-new-repo -c -d "My project files" *.apk

# Create a private repository
./github-upload -r private-repo -c --private data.csv
```

---

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--repo` | `-r` | Repository name (`user/repo` or just `repo`) |
| `--message` | `-m` | Commit message |
| `--branch` | `-b` | Target branch (default: main) |
| `--create` | `-c` | Create repository if it doesn't exist |
| `--description` | `-d` | Repository description (used with `--create`) |
| `--public` | | Make new repo public (default) |
| `--private` | | Make new repo private |
| `--help` | `-h` | Show help message |

---

## Examples

### Basic Upload

```bash
./github-upload -r myname/myrepo document.pdf
```

### Batch Upload

```bash
./github-upload -r myname/myrepo file1.txt file2.txt images/*
```

### Upload with Auto-Repo Creation

```bash
./github-upload -r my-new-project -c "My backup" backup.tar.gz
```

### Update a Specific Branch

```bash
./github-upload -r myname/myrepo -b dev -m "Update dev build" app-debug.apk
```

### Private Repository

```bash
./github-upload -r myname/private-repo -c --private secrets.txt
```

### View Repository After Upload

```bash
./github-upload -r myname/myrepo image.png
# Opens: https://github.com/myname/myrepo
```

---

## Config Files

Credentials are stored at:
```
~/.config/github-upload/config
```

State files (if any) are at:
```
~/.cache/github-upload/state
```

---

## Troubleshooting

### "gh: command not found"

Install GitHub CLI first — see [Requirements](#requirements).

### "Repository not found"

Use `-c` flag to create the repository automatically:
```bash
./github-upload -r new-repo -c file.txt
```

### Authentication failed

Make sure your token has the **`repo`** scope. Check your tokens at:
https://github.com/settings/tokens

### Permission denied

Your token may be expired or lack permissions. Generate a new token with `repo` scope.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.
