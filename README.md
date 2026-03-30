# GitHub Upload Tool

> Simple, powerful file upload to GitHub from any terminal.

A modern bash script that makes uploading files to GitHub repositories effortless. Supports multiple accounts, smart repository detection, and both interactive menu and command-line modes.

- ✅ Works on Termux, Linux, macOS, WSL
- ✅ Multiple GitHub accounts with auto-detection
- ✅ Create repos on the fly
- ✅ No git commands needed — just run and upload

---

## ✨ Features

- **Multi-Account Support** — Configure multiple GitHub accounts. The tool auto-detects which account has access to a repository and lets you choose when multiple accounts can access it.
- **Smart Repo Creation** — When a repository doesn't exist, pick which account should create it.
- **Interactive Menu** — User-friendly menu for beginners.
- **Fully Scriptable** — All flags supported for automation.
- **Secure** — Credentials stored with `600` permissions, never logged.
- **Any File Type** — Upload APKs, PDFs, images, archives, anything.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/papi144/Uplode-tools-to-github-.git
cd Uplode-tools-to-github-

# Make executable
chmod +x github-upload

# Optional: install to PATH
sudo mv github-upload /usr/local/bin/
```

**Requirements:** `git`, `curl`. No need for `gh` CLI anymore.

---

## 🔐 Authentication

First run will prompt for your GitHub credentials:

```bash
./github-upload
```

```
GitHub username: your_username
GitHub Personal Access Token: ghp_xxxxxxxxxxxx
```

Credentials are saved to:
- Default account: `~/.config/github-upload/config`
- Additional accounts: `~/.config/github-upload/accounts/<name>/config`

### Create a Token

1. Go to **GitHub Settings → Personal Access Tokens → Tokens (classic)**
2. **Generate new token**
3. Select **`repo`** scope (full control of private repositories)
4. Copy the token (starts with `ghp_`)

---

## 🚀 Usage

### Interactive Mode (Menu)

```bash
./github-upload
```

Shows a menu:
1. **Upload files** — Select repository and files interactively
2. **Add another account** — Add more GitHub accounts
3. **List accounts** — See configured accounts
4. **Quit**

### Direct Mode (Command Line)

```bash
# Basic upload
./github-upload -r user/repo file.txt

# Upload multiple files
./github-upload -r user/repo file1.pdf file2.png backup.zip

# Custom commit message
./github-upload -r user/repo -m "Update documentation" README.md

# Use a specific branch
./github-upload -r user/repo -b develop app.apk

# Create a new repository and upload
./github-upload -c -r new-repo-name *.apk

# Create a private repository
./github-upload -c -r private-repo --private secrets.json

# Force a specific account
./github-upload -a work -r company/project file.zip

# Add a new account (non-interactive if name provided)
./github-upload -A personal
```

---

## 🔧 Options

| Option | Description |
|--------|-------------|
| `-r, --repo REPO` | Repository (`user/repo` or just `repo`) |
| `-m, --message MSG` | Commit message (default: "Upload files via github-upload") |
| `-b, --branch BRANCH` | Target branch (default: repository's default) |
| `-a, --account NAME` | Use specific account (default: auto-detect) |
| `-A, --add-account [NAME]` | Add a new account (prompts if no name) |
| `-c, --create` | Create repository if missing |
| `-d, --description DESC` | Repository description (with `-c`) |
| `--public` | Make new repo public (default) |
| `--private` | Make new repo private |
| `-h, --help` | Show help |

---

## 🤔 How Multi-Account Works

1. **Add accounts** once: `./github-upload -A personal`, `./github-upload -A work`
2. **Upload**: `./github-upload -r some/repo file.txt`
   - Script checks all configured accounts for access
   - If **one** account has access → uses it
   - If **multiple** accounts have access → you choose which to use
   - If **none** have access and `-c` used → you choose which account creates it
3. **Credentials are reused** — no re-entering tokens

---

## 📝 Examples

### Upload a backup archive
```bash
./github-upload -r myuser/backups -c -d "Daily backup" backup_$(date +%Y%m%d).tar.gz
```

### Multiple accounts scenario
```bash
./github-upload -A personal    # Enter personal account tokens
./github-upload -A work        # Enter work account tokens

# Upload to personal repo (auto-detected)
./github-upload -r personaluser/personal-repo photo.jpg

# Upload to work repo (auto-detected) or choose if both have access
./github-upload -r company/work-repo report.pdf

# Force using work account
./github-upload -a work -r company/work-repo report.pdf
```

---

## 🛠️ Configuration Files

- Default account: `~/.config/github-upload/config`
- Named accounts: `~/.config/github-upload/accounts/<name>/config`
- Environment overrides: `GITHUB_USERNAME`, `GITHUB_TOKEN`, or `GITHUB_USERNAME_<NAME>`, `GITHUB_TOKEN_<NAME>`

---

## ❓ Troubleshooting

**"Repository not found"**
- Use `-c` to create it: `./github-upload -c -r new-repo file.txt`
- Or check you have access with the selected account

**"Permission denied"**
- Token may be expired or lack `repo` scope. Generate a new token.

**"No accounts configured"**
- Run `./github-upload -A` to add an account

**Branch not found**
- The script will create the specified branch automatically

---

## 📄 License

MIT © 2026

---

**Enjoy uploading!** 🚀