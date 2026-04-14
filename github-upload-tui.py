#!/usr/bin/env python3
"""
GitHub Direct Upload Tool - TUI Version
Works on: Linux, Windows, Termux, macOS, VPS
"""

import os
import sys
import base64
import json
from pathlib import Path

# Check for required libraries
try:
    import requests
except ImportError:
    print("Error: 'requests' library not needed. Installing...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

try:
    from rich.console import Console
    from rich.table import Table
    from rich.tree import Tree
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.menu import Menu
    from rich import box
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    # Fallback to simple CLI
    console = None

# Configuration
CONFIG_DIR = os.path.expanduser("~/.config/github-upload")
DEFAULT_CONFIG = os.path.join(CONFIG_DIR, "config")
ACCOUNTS_DIR = os.path.join(CONFIG_DIR, "accounts")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }
    
    def verify_account(self):
        response = requests.get("https://api.github.com/user", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None
    
    def list_repos(self):
        response = requests.get("https://api.github.com/user/repos?per_page=100", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []
    
    def list_files(self, repo):
        response = requests.get(f"https://api.github.com/repos/{repo}/contents", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None
    
    def create_repo(self, name, private=False, description=""):
        data = {"name": name, "private": private}
        if description:
            data["description"] = description
        response = requests.post("https://api.github.com/user/repos", headers=self.headers, json=data)
        return response.status_code in [200, 201]
    
    def upload_file(self, repo, file_path, repo_path=None, message="Upload"):
        if repo_path is None:
            repo_path = os.path.basename(file_path)
        
        with open(file_path, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        
        # Check if file exists
        check_response = requests.get(f"https://api.github.com/repos/{repo}/contents/{repo_path}", headers=self.headers)
        sha = ""
        if check_response.status_code == 200:
            sha = check_response.json().get("sha", "")
        
        data = {"message": message, "content": content}
        if sha:
            data["sha"] = sha
        
        response = requests.put(f"https://api.github.com/repos/{repo}/contents/{repo_path}", 
                                 headers=self.headers, json=data)
        return response.status_code in [200, 201]
    
    def delete_file(self, repo, file_path, message="Delete"):
        response = requests.get(f"https://api.github.com/repos/{repo}/contents/{file_path}", headers=self.headers)
        if response.status_code != 200:
            return False
        
        sha = response.json().get("sha", "")
        data = {"message": message, "sha": sha}
        
        response = requests.delete(f"https://api.github.com/repos/{repo}/contents/{file_path}", 
                                  headers=self.headers, json=data)
        return response.status_code in [200, 204]
    
    def get_repo_tree(self, repo):
        """Get repository as a tree structure"""
        contents = self.list_files(repo)
        if not contents:
            return None
        return contents


class GitHubTUI:
    def __init__(self):
        self.accounts = self.load_accounts()
        self.current_account = self.get_default_account()
        self.github = None
        if self.current_account:
            self.load_account_api(self.current_account)
    
    def load_accounts(self):
        accounts = {}
        
        if os.path.exists(DEFAULT_CONFIG):
            with open(DEFAULT_CONFIG, "r") as f:
                content = f.read()
                data = {"username": "", "token": ""}
                for line in content.split("\n"):
                    if "GITHUB_USERNAME" in line:
                        data["username"] = line.split("=")[1].strip().strip('"')
                    elif "GITHUB_TOKEN" in line:
                        data["token"] = line.split("=")[1].strip().strip('"')
                if data["username"]:
                    accounts["default"] = data
        
        if os.path.exists(ACCOUNTS_DIR):
            for folder in os.listdir(ACCOUNTS_DIR):
                config_file = os.path.join(ACCOUNTS_DIR, folder, "config")
                if os.path.exists(config_file):
                    with open(config_file, "r") as f:
                        content = f.read()
                        data = {"username": "", "token": ""}
                        for line in content.split("\n"):
                            if "GITHUB_USERNAME" in line:
                                data["username"] = line.split("=")[1].strip().strip('"')
                            elif "GITHUB_TOKEN" in line:
                                data["token"] = line.split("=")[1].strip().strip('"')
                        if data["username"]:
                            accounts[folder] = data
        
        return accounts
    
    def get_default_account(self):
        if "default" in self.accounts:
            return "default"
        keys = list(self.accounts.keys())
        return keys[0] if keys else None
    
    def save_account(self, name, username, token):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        if name == "default":
            config_file = DEFAULT_CONFIG
        else:
            os.makedirs(ACCOUNTS_DIR, exist_ok=True)
            config_file = os.path.join(ACCOUNTS_DIR, name, "config")
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, "w") as f:
            f.write(f'GITHUB_USERNAME="{username}"\n')
            f.write(f'GITHUB_TOKEN="{token}"\n')
        
        os.chmod(config_file, 0o600)
        self.accounts = self.load_accounts()
    
    def load_account_api(self, acc_name):
        if acc_name in self.accounts:
            self.github = GitHubAPI(self.accounts[acc_name]["token"])
            return True
        return False
    
    def print_header(self):
        if HAS_RICH:
            console.clear()
            console.print(Panel("[bold cyan]GitHub Upload Tool - TUI v1.0[/bold cyan]\n[dim]Works on: Linux, Windows, Termux, macOS[/dim]", 
                               box=box.DOUBLE, style="cyan"))
        else:
            print("\n" + "="*50)
            print("  GitHub Upload Tool - TUI v1.0")
            print("  Works on: Linux, Windows, Termux, macOS")
            print("="*50)
    
    def show_accounts(self):
        if HAS_RICH:
            table = Table(title="Available Accounts", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Username", style="yellow")
            
            for i, (name, data) in enumerate(self.accounts.items(), 1):
                marker = " [◉]" if name == self.current_account else ""
                table.add_row(str(i), name + marker, data.get("username", "N/A"))
            
            console.print(table)
        else:
            print("\nAvailable Accounts:")
            for i, (name, data) in enumerate(self.accounts.items(), 1):
                marker = " (current)" if name == self.current_account else ""
                print(f"  {i}. {name}{marker}: {data.get('username', 'N/A')}")
    
    def select_account(self):
        self.show_accounts()
        if HAS_RICH:
            choice = Prompt.ask("[cyan]Select account[/cyan]", choices=[str(i) for i in range(1, len(self.accounts)+1)], default="1")
        else:
            choice = input("Select account: ")
        
        idx = int(choice) - 1
        acc_name = list(self.accounts.keys())[idx]
        
        if self.load_account_api(acc_name):
            self.current_account = acc_name
            return True
        return False
    
    def show_repos(self, account_name=None):
        if not self.github:
            if not self.select_account():
                return
        
        user = self.github.verify_account()
        if not user:
            print("[x] Invalid token!")
            return
        
        repos = self.github.list_repos()
        
        if HAS_RICH:
            table = Table(title=f"Repositories for {user['login']}", box=box.ROUNDED)
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Description", style="yellow")
            
            for repo in repos:
                table.add_row(
                    repo["name"],
                    "[red]private[/red]" if repo["private"] else "[green]public[/green]",
                    repo.get("description", "-")[:50]
                )
            
            console.print(table)
            console.print(f"\n[bold]Total:[/bold] {len(repos)} repositories")
        else:
            print(f"\nRepositories for {user['login']}:")
            print("-" * 50)
            for repo in repos:
                pvt = "private" if repo["private"] else "public"
                desc = repo.get("description", "-")[:40]
                print(f"  {repo['name']} ({pvt}) - {desc}")
            print(f"\nTotal: {len(repos)} repos")
    
    def show_repo_tree(self, repo_name):
        if not self.github:
            print("[!] No account selected!")
            return
        
        # Expand repo name if needed
        if "/" not in repo_name:
            username = self.accounts[self.current_account]["username"]
            repo_name = f"{username}/{repo_name}"
        
        contents = self.github.get_repo_tree(repo_name)
        
        if not contents:
            print("[!] Repository not found or empty!")
            return
        
        if HAS_RICH:
            tree = Tree(f"[bold cyan]📁 {repo_name}[/bold cyan]")
            
            for item in contents:
                if item["type"] == "dir":
                    tree.add(f"[blue]📂 {item['name']}/[/blue]")
                else:
                    size = item.get("size", 0)
                    if size < 1024:
                        size_str = f"{size}B"
                    elif size < 1024*1024:
                        size_str = f"{size/1024:.1f}KB"
                    else:
                        size_str = f"{size/1024/1024:.1f}MB"
                    tree.add(f"[green]📄 {item['name']}[/green] ({size_str})")
            
            console.print(tree)
        else:
            print(f"\nFiles in {repo_name}:")
            print("-" * 40)
            for item in contents:
                if item["type"] == "dir":
                    print(f"  📂 {item['name']}/")
                else:
                    print(f"  📄 {item['name']}")
    
    def add_account(self):
        print("\n[Add New Account]")
        name = input("Account name (e.g., work, personal): ").strip()
        if not name:
            print("[x] Account name required!")
            return
        
        username = input("GitHub username: ").strip()
        if not username:
            print("[x] Username required!")
            return
        
        import getpass
        token = getpass.getpass("GitHub token (with repo scope): ")
        if not token:
            print("[x] Token required!")
            return
        
        self.save_account(name, username, token)
        print(f"[✓] Account '{name}' saved!")
    
    def create_repo(self):
        if not self.github:
            if not self.select_account():
                return
        
        name = input("\nRepository name: ").strip()
        if not name:
            print("[x] Repository name required!")
            return
        
        desc = input("Description (optional): ").strip()
        private = input("Make private? (y/N): ").strip().lower() == 'y'
        
        if self.github.create_repo(name, private, desc):
            print(f"[✓] Repository '{name}' created!")
        else:
            print("[x] Failed to create repository!")
    
    def upload_file(self):
        if not self.github:
            if not self.select_account():
                return
        
        file_path = input("\nFile path to upload: ").strip()
        if not file_path or not os.path.exists(file_path):
            print("[x] File not found!")
            return
        
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            print(f"[x] File too large! Max: 100MB")
            return
        
        repo = input("Repository (user/repo or just repo name): ").strip()
        if not repo:
            print("[x] Repository required!")
            return
        
        # Expand repo if needed
        if "/" not in repo:
            username = self.accounts[self.current_account]["username"]
            repo = f"{username}/{repo}"
        
        msg = input("Commit message: ").strip()
        if not msg:
            msg = f"Upload {os.path.basename(file_path)}"
        
        print(f"\nUploading to {repo}...")
        if self.github.upload_file(repo, file_path, message=msg):
            print("[✓] File uploaded successfully!")
            print(f"   View at: https://github.com/{repo}")
        else:
            print("[x] Upload failed!")
    
    def show_menu(self):
        if HAS_RICH:
            console.print("\n[bold cyan]Main Menu:[/bold cyan]")
            console.print("  [1] 👤 Add new account")
            console.print("  [2] 📋 List accounts")
            console.print("  [3] 🔄 Switch account")
            console.print("  [4] 📁 List my repositories")
            console.print("  [5] 🌳 View repo tree (graph)")
            console.print("  [6] 📤 Upload file")
            console.print("  [7] ➕ Create repository")
            console.print("  [8] 🗑️  Delete file")
            console.print("  [9] ❌ Exit")
        else:
            print("\nMain Menu:")
            print("  1. Add new account")
            print("  2. List accounts")
            print("  3. Switch account")
            print("  4. List my repositories")
            print("  5. View repo tree (graph)")
            print("  6. Upload file")
            print("  7. Create repository")
            print("  8. Delete file")
            print("  9. Exit")
    
    def run(self):
        while True:
            self.print_header()
            
            if self.current_account and self.accounts.get(self.current_account):
                user = self.accounts[self.current_account]["username"]
                if HAS_RICH:
                    console.print(f"\n[green]Logged in as:[/green] [bold]{user}[/bold]")
                else:
                    print(f"\nLogged in as: {user}")
            
            self.show_menu()
            
            if HAS_RICH:
                choice = Prompt.ask("[cyan]Select option[/cyan]", choices=["1","2","3","4","5","6","7","8","9"], default="9")
            else:
                choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.add_account()
            elif choice == "2":
                self.show_accounts()
            elif choice == "3":
                self.select_account()
            elif choice == "4":
                self.show_repos()
            elif choice == "5":
                repo = input("Enter repo name: ").strip()
                if repo:
                    self.show_repo_tree(repo)
            elif choice == "6":
                self.upload_file()
            elif choice == "7":
                self.create_repo()
            elif choice == "8":
                self.delete_file()
            elif choice == "9":
                print("\nGoodbye!")
                break
            
            input("\nPress Enter to continue...")
    
    def delete_file(self):
        if not self.github:
            if not self.select_account():
                return
        
        repo = input("\nRepository: ").strip()
        file_path = input("File path to delete: ").strip()
        
        if not repo or not file_path:
            print("[x] Repository and file path required!")
            return
        
        # Expand repo if needed
        if "/" not in repo:
            username = self.accounts[self.current_account]["username"]
            repo = f"{username}/{repo}"
        
        msg = input("Commit message (optional): ").strip()
        if not msg:
            msg = f"Delete {file_path}"
        
        if Confirm.ask(f"Delete {file_path} from {repo}?", default=False) if HAS_RICH else input(f"Delete {file_path}? (y/N): ").lower() == 'y':
            if self.github.delete_file(repo, file_path, msg):
                print("[✓] File deleted!")
            else:
                print("[x] Failed to delete!")


def main():
    if not HAS_RICH:
        print("Warning: 'rich' library not found. Using simple text mode.")
        print("Install rich for better UI: pip install rich")
        print()
    
    app = GitHubTUI()
    
    if not app.accounts:
        print("\nNo accounts found! Let me help you add one.")
        app.add_account()
    
    app.run()


if __name__ == "__main__":
    main()