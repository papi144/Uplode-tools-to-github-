# GitHub Direct Upload Tool

> Upload files to GitHub **directly via API** - No git clone needed!

A powerful bash script that uploads files to GitHub repositories using the GitHub API. Fast, simple, and works on any system with `curl` and `jq`.

## ✨ Features

- 🚀 **Direct API Upload** - No git clone, no git commands needed
- ⚡ **Fast** - Uploads directly to GitHub servers
- 📁 **Upload Any File** - APKs, PDFs, images, archives, anything!
- 🔄 **Update Files** - Automatically detects and updates existing files
- 🗑️ **Delete Files** - Remove files from repositories
- 📋 **List Files** - View files in any repository
- 🔇 **Quiet Mode** - Minimal output for scripting
- 💾 **Multi-Account** - Support for multiple GitHub accounts
- 🔒 **Secure** - Credentials stored with proper permissions
- 📦 **100MB Max** - Upload files up to 100MB

## 📦 Requirements

- `bash` (4.0+)
- `curl`
- `jq`
- `GitHub Personal Access Token` with `repo` scope

## 🔧 Installation

### Linux / VPS / Server

```bash
# Download the script
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github-/main/github-upload

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
# Download the script
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github-/main/github-upload

# Make it executable
chmod +x github-upload

# Optional: Install to PATH
mkdir -p ~/bin
mv github-upload ~/bin/
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Android (Termux)

```bash
# Install dependencies
pkg install curl jq

# Download the script
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github-/main/github-upload

# Make it executable
chmod +x github-upload
```

### Windows (WSL) - Recommended

```bash
# Install WSL if not already
wsl --install

# Then in WSL terminal:
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github-/main/github-upload
chmod +x github-upload
./github-upload -A
```

### Windows (Git Bash)

```bash
# Download using curl
curl -O https://raw.githubusercontent.com/papi144/Uplode-tools-to-github-/main/github-upload

# Make it executable
chmod +x github-upload

# Run
./github-upload -A
```

### Windows (PowerShell)

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/papi144/Uplode-tools-to-github-/main/github-upload" -OutFile "github-upload"
```

### From Source

```bash
git clone https://github.com/papi144/Uplode-tools-to-github-.git
cd Uplode-tools-to-github-
chmod +x github-upload
sudo mv github-upload /usr/local/bin/
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

### Secure Token Storage

#### Option 1: Environment Variable (Recommended)
```bash
# Add to ~/.bashrc or ~/.profile
export GITHUB_TOKEN="ghp_yourtoken"
export GITHUB_USERNAME="yourusername"

# Source it
source ~/.bashrc
```

#### Option 2: System Keychain (Linux)
```bash
# Install keychain
apt install keychain

# Add token
keychain --eval github.token ghp_yourtoken >> ~/.bashrc

# Add to ~/.bashrc
eval $(keychain --eval github.token)
```

#### Option 3: macOS Keychain
```bash
# Store in Keychain
security add-internet-password -s github.com -a username -w "ghp_yourtoken"
```

## 🚀 Usage

### Basic Commands

```bash
# Upload a file (creates repo if needed)
github-upload -r my-repo -c myfile.apk

# Upload to existing repo
github-upload -r username/my-repo myfile.apk

# Upload with custom message
github-upload -r my-repo -m "Version 2.0" app.apk

# Upload multiple files
github-upload -r my-repo file1.txt file2.png file3.pdf

# Upload with wildcard
github-upload -r my-repo '*.apk'
```

### Create Repository Options

```bash
# Create public repo
github-upload -r my-app -c myfile.apk

# Create private repo
github-upload -r my-app --private -c myfile.apk

# Create with description
github-upload -r my-app -c -d "My App Description" myfile.apk
```

### File Management

```bash
# Upload to custom path in repo
github-upload -r my-repo -f "apps/v2/app.apk" app.apk

# List files in repo
github-upload -r my-repo --list

# List files in subfolder
github-upload -r my-repo --list folder/subfolder

# Delete a file
github-upload -r my-repo --delete oldfile.txt

# Delete file with custom message
github-upload -r my-repo --delete oldfile.txt -m "Remove deprecated file"
```

### Advanced Options

```bash
# Quiet mode (minimal output)
github-upload -r my-repo -q *.apk

# Dry run (preview what would be uploaded)
github-upload -r my-repo -n *.apk

# Use specific account
github-upload -a work -r company/repo file.zip

# Update existing file
github-upload -r my-repo -m "Updated" myfile.apk
```

## 📝 Command Reference

| Option | Description |
|--------|-------------|
| `-r, --repo REPO` | Repository name (`repo` or `user/repo`) |
| `-c, --create` | Create repository if it doesn't exist |
| `-p, --private` | Make new repository private |
| `-d, --description TEXT` | Repository description (with `-c`) |
| `-m, --message TEXT` | Commit message |
| `-f, --file-path PATH` | Upload to custom path in repo |
| `-A, --add-account` | Add a new GitHub account |
| `-a, --account NAME` | Use specific account |
| `--list-accounts` | List all saved accounts |
| `--list [PATH]` | List files in repository |
| `--list-repos` | List your repositories |
| `--list-branches` | List branches in repository |
| `-b, --branch NAME` | Create new branch |
| `--delete PATH` | Delete a file from repository |
| `-q, --quiet` | Quiet mode (minimal output) |
| `-n, --dry-run` | Show what would be uploaded |
| `--clear` | Clear saved credentials |
| `-h, --help` | Show help |

## 📁 Configuration

Credentials are stored in:
- **Default account:** `~/.config/github-upload/config`
- **Additional accounts:** `~/.config/github-upload/accounts/NAME/config`

Permissions are set to `600` (owner read/write only) for security.

## 💡 Examples

### Upload an APK

```bash
github-upload -r my-android-app -c -m "v1.0.0 release" app.apk
```

### Upload Multiple Files

```bash
github-upload -r backup-repo -m "Daily backup" file1.zip file2.tar
```

### Update App with New Version

```bash
github-upload -r my-app -m "Updated to v2.0" app.apk
```

### Upload All APKs from Folder

```bash
github-upload -r android-apps -c -m "All apps" ./downloads/*.apk
```

### Organize Files with Paths

```bash
github-upload -r my-repo \
  -f "images/icons/app.png" icon.png \
  -f "images/screenshots/s1.png" screenshot1.png \
  -f "images/screenshots/s2.png" screenshot2.png
```

### Backup Configuration

```bash
github-upload -r my-configs -c -d "System configurations" \
  ~/.ssh/config \
  ~/.gitconfig \
  .bashrc
```

### Delete Old Files

```bash
# Delete single file
github-upload -r my-repo --delete old-version.apk

# Delete multiple files
github-upload -r my-repo --delete temp1.tmp
github-upload -r my-repo --delete temp2.tmp
```

### List Your Repositories

```bash
github-upload --list-repos
```

### List Branches

```bash
# List branches in a repository
github-upload -r my-repo --list-branches
```

### Create Branch

```bash
# Create new branch from main
github-upload -r my-repo -b feature-branch

# Create branch from specific branch
github-upload -r my-repo -b dev-branch --source-branch develop
```

## 🔍 Troubleshooting

### "No account configured"

Run `github-upload -A` to add your GitHub account.

### "Repository not found"

Use `-c` flag to create the repository:
```bash
github-upload -r new-repo -c myfile.apk
```

### "File too large"

Maximum file size is 100MB. For larger files, use Git LFS or split the file.

### "Permission denied"

Check your token has `repo` scope. Generate a new token at:
https://github.com/settings/tokens

### "Invalid token"

Verify your token is correct. Run:
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

Pull requests welcome! Please read contributing guidelines first.

## 📧 Contact

- GitHub: [@papi144](https://github.com/papi144)
- Issues: [Open an issue](https://github.com/papi144/Uplode-tools-to-github-/issues)

---

**Enjoy!**
