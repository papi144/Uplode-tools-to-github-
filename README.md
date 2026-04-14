# GitHub Direct Upload Tool

> Upload files to GitHub **directly via API** - No git clone needed!

A powerful bash script that uploads files to GitHub repositories using the GitHub API. Fast, simple, and works on any system with `curl`.

## ✨ Features

- 🚀 **Direct API Upload** - No git clone, no git commands needed
- ⚡ **Fast** - Uploads directly to GitHub servers
- 📁 **Upload Any File** - APKs, PDFs, images, archives, anything!
- 🔄 **Update Files** - Automatically detects and updates existing files
- 🗑️ **Delete Files** - Remove files from repositories
- 📋 **List Files** - View files in any repository
- 🌳 **Graph/Tree View** - Visual representation of repos and files
- 🔢 **Account Selection** - Numbered menu for easy account switching
- 📄 **File Type Icons** - Different emojis for different file types
- 🔇 **Quiet Mode** - Minimal output for scripting
- 💾 **Multi-Account** - Support for multiple GitHub accounts
- 🔒 **Secure** - Credentials stored with proper permissions
- 📦 **100MB Max** - Upload files up to 100MB

## 📦 Requirements

- `bash` (4.0+)
- `curl`
- `jq` (optional - works without it)
- `GitHub Personal Access Token` with `repo` scope

## 🔧 Installation

### Linux / VPS / Server

```bash
# Option 1: Download with curl
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github/main/github-upload

# Option 2: Clone with git
git clone https://github.com/papi144/Uplode-tools-to-github.git
cd Uplode-tools-to-github

# Make it executable
chmod +x github-upload

# Optional: Install to PATH
mkdir -p ~/bin
mv github-upload ~/bin/
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### macOS

```bash
# Option 1: Download with curl
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github/main/github-upload

# Option 2: Clone with git
git clone https://github.com/papi144/Uplode-tools-to-github.git
cd Uplode-tools-to-github

# Make it executable
chmod +x github-upload
```

### Android (Termux)

```bash
# Install dependencies
pkg install curl jq git

# Download
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github/main/github-upload

# Or clone
git clone https://github.com/papi144/Uplode-tools-to-github.git
cd Uplode-tools-to-github

chmod +x github-upload
```

### Windows (WSL)

```bash
# Install WSL if not already
wsl --install

# Then in WSL:
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github/main/github-upload
chmod +x github-upload
./github-upload -A
```

### Windows (Git Bash)

```bash
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github/main/github-upload
chmod +x github-upload
./github-upload -A
```

## 🔐 Setup

### 1. Create a GitHub Token

1. Go to **GitHub → Settings → Developer settings**
2. **Personal access tokens → Tokens (classic)**
3. **Generate new token**
4. Select **`repo`** scope (full control of repositories)
5. Copy the token (starts with `ghp_`)

### 2. Add Your Account

```bash
# Interactive (will ask for username and token)
github-upload -A

# Or non-interactive
echo "GITHUB_USERNAME=yourusername" > ~/.config/github-upload/config
echo "GITHUB_TOKEN=ghp_yourtoken" >> ~/.config/github-upload/config
chmod 600 ~/.config/github-upload/config
```

## 🚀 Usage

### Interactive Menu (No Arguments)

```bash
# Run without arguments to see interactive menu
./github-upload
```

Menu options:
1. Add new account
2. List available accounts
3. Remove account
4. Switch default account
5. Upload file(s)
6. List files in repository
7. Create new repository
8. List my repositories
9. List repos for specific account
10. Delete file from repository
11. **See graph (tree view)** ← Shows repos and files visually!
12. Exit

### Basic Commands

```bash
# Upload a file (creates repo if needed)
github-upload -r my-repo -c myfile.apk

# Upload with custom message
github-upload -r my-repo -m "Version 2.0" app.apk

# Upload to specific path
github-upload -r my-repo -f "apps/android/app.apk" app.apk

# Upload multiple files
github-upload -r my-repo app.apk icon.png readme.txt

# Create private repo and upload
github-upload -r my-repo -c -p -d "My app" app.apk

# Delete a file
github-upload -r my-repo --delete old-file.txt

# List files in repo
github-upload -r my-repo --list

# List your repositories
github-upload --list-repos

# Add new account
github-upload -A

# Use specific account
github-upload -a work -r company/repo file.txt
```

### Graph/Tree View (Option 11)

```bash
# Run interactively, select option 11
./github-upload
# Then select 11 to see all repos with file tree!
```

Shows:
```
╔══════════════════════════════════════════════════════════╗
║        📁 REPOSITORIES FOR papi144              ║
╚══════════════════════════════════════════════════════════╝

┌─ 📂 my-repo
│   ├── 🐍 main.py
│   ├── 📄 README.md
│   └── 📄 requirements.txt
│
┌─ 📂 another-repo
│   ├── 📦 app.apk
│   └── 🖼️ icon.png
│
Total: 2 repositories
```

### File Type Emojis

Different files show different icons:
- 📦 APK, IPA, Linux packages
- 🐍 Python (.py)
- 🖼️ Images (.png, .jpg, .gif)
- 📄 Text files
- 🗜️ Archives (.zip, .rar)
- 🎵 Audio
- 🎬 Video

## 📋 All Options

| Option | Description |
|--------|-------------|
| `-r, --repo` | Repository name |
| `-c, --create` | Create repository if not exists |
| `-p, --private` | Make repository private |
| `-d, --description` | Repository description |
| `-m, --message` | Commit message |
| `-f, --file-path` | Upload to specific path |
| `-A, --add-account` | Add new account |
| `-a, --account` | Use specific account |
| `--list-accounts` | Show saved accounts |
| `--delete` | Delete file from repo |
| `--list` | List files in repo |
| `--list-repos` | List your repositories |
| `--list-branches` | List branches in repo |
| `-b, --branch` | Create new branch |
| `-q, --quiet` | Quiet mode |
| `-P, --progress` | Show progress bar |
| `-n, --dry-run` | Show what would be uploaded |
| `-h, --help` | Show help |
| `--clear` | Clear saved credentials |

## 🔍 Troubleshooting

### "No account configured"
Run `github-upload -A` to add your GitHub account.

### "Repository not found"
Use `-c` flag to create the repository:
```bash
github-upload -r new-repo -c myfile.apk
```

### "File too large"
Maximum file size is 100MB.

### "Permission denied"
Check your token has `repo` scope.

### "Invalid token"
Verify your token is correct:
```bash
github-upload --list-accounts
```

If issues persist, clear and re-add:
```bash
github-upload --clear
github-upload -A
```

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🌐 Works On

| Platform | Status |
|----------|--------|
| Linux (all distros) | ✅ |
| macOS | ✅ |
| Windows (WSL) | ✅ |
| Windows (Git Bash) | ✅ |
| Android (Termux) | ✅ |
| VPS / Servers | ✅ |

## 🤝 Contributing

Pull requests welcome!

## 📧 Contact

- GitHub: [@papi144](https://github.com/papi144)
- Issues: [Open an issue](https://github.com/papi144/Uplode-tools-to-github/issues)

---

**Enjoy!**