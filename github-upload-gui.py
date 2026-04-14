#!/usr/bin/env python3
"""
GitHub Direct Upload Tool - GUI Version
Works on: Linux, Windows, Termux, macOS
"""

import os
import sys
import base64
import json
import subprocess
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

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


class GitHubGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitHub Upload Tool v1.0")
        self.root.geometry("800x600")
        self.accounts = self.load_accounts()
        self.current_account = self.get_default_account()
        
        self.setup_ui()
    
    def load_accounts(self):
        accounts = {}
        
        if os.path.exists(DEFAULT_CONFIG):
            with open(DEFAULT_CONFIG, "r") as f:
                content = f.read()
                for line in content.split("\n"):
                    if "GITHUB_USERNAME" in line:
                        accounts["default"] = {"username": line.split("=")[1].strip().strip('"')}
                    elif "GITHUB_TOKEN" in line:
                        accounts["default"]["token"] = line.split("=")[1].strip().strip('"')
        
        if os.path.exists(ACCOUNTS_DIR):
            for folder in os.listdir(ACCOUNTS_DIR):
                config_file = os.path.join(ACCOUNTS_DIR, folder, "config")
                if os.path.exists(config_file):
                    with open(config_file, "r") as f:
                        content = f.read()
                        acc_data = {"username": "", "token": ""}
                        for line in content.split("\n"):
                            if "GITHUB_USERNAME" in line:
                                acc_data["username"] = line.split("=")[1].strip().strip('"')
                            elif "GITHUB_TOKEN" in line:
                                acc_data["token"] = line.split("=")[1].strip().strip('"')
                        if acc_data["username"]:
                            accounts[folder] = acc_data
        
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
        messagebox.showinfo("Success", f"Account '{name}' saved!")
    
    def setup_ui(self):
        # Main menu
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(self.main_frame, text="GitHub Upload Tool - GUI", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Account selection
        ttk.Label(self.main_frame, text="Account:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.account_var = tk.StringVar(value=self.current_account or "")
        self.account_combo = ttk.Combobox(self.main_frame, textvariable=self.account_var, values=list(self.accounts.keys()))
        self.account_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Action buttons
        ttk.Label(self.main_frame, text="Actions:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(btn_frame, text="Add Account", command=self.add_account_gui).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="List Repos", command=self.list_repos_gui).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Upload File", command=self.upload_file_gui).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Create Repo", command=self.create_repo_gui).pack(side=tk.LEFT, padx=2)
        
        # Output area
        ttk.Label(self.main_frame, text="Output:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.output_text = tk.Text(self.main_frame, height=20, width=80)
        self.output_text.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.grid(row=4, column=2, sticky=(tk.N, tk.S))
        self.output_text.config(yscrollcommand=scrollbar.set)
    
    def output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
    
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
    
    def get_current_account(self):
        acc_name = self.account_var.get()
        if not acc_name or acc_name not in self.accounts:
            messagebox.showerror("Error", "No account selected!")
            return None
        
        acc = self.accounts[acc_name]
        if not acc.get("token"):
            token = tk.simpledialog.askstring("Token Required", "Enter GitHub token for this account:", show="*")
            if token:
                acc["token"] = token
                self.save_account(acc_name, acc["username"], token)
            else:
                return None
        
        return acc
    
    def add_account_gui(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Account")
        dialog.geometry("400x250")
        
        ttk.Label(dialog, text="Account Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="GitHub Username:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        user_entry = ttk.Entry(dialog, width=30)
        user_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="GitHub Token:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        token_entry = ttk.Entry(dialog, width=30, show="*")
        token_entry.grid(row=2, column=1, padx=10, pady=5)
        
        def save():
            name = name_entry.get().strip()
            user = user_entry.get().strip()
            token = token_entry.get().strip()
            
            if not name or not user or not token:
                messagebox.showerror("Error", "All fields required!")
                return
            
            self.save_account(name, user, token)
            self.account_combo["values"] = list(self.accounts.keys())
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=20)
    
    def list_repos_gui(self):
        acc = self.get_current_account()
        if not acc:
            return
        
        self.clear_output()
        
        try:
            api = GitHubAPI(acc["token"])
            user = api.verify_account()
            if not user:
                self.output("[x] Invalid token!")
                messagebox.showerror("Error", "Invalid token!")
                return
            
            repos = api.list_repos()
            self.output(f"Repositories for {user['login']}:")
            self.output("-" * 40)
            for repo in repos:
                self.output(f"  {repo['name']} {'(private)' if repo['private'] else '(public)'}")
            
            self.output(f"\nTotal: {len(repos)} repos")
        except Exception as e:
            self.output(f"[x] Error: {str(e)}")
    
    def upload_file_gui(self):
        acc = self.get_current_account()
        if not acc:
            return
        
        file_path = filedialog.askopenfilename(title="Select file to upload")
        if not file_path:
            return
        
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            messagebox.showerror("Error", f"File too large! Max: 100MB")
            return
        
        repo = tk.simpledialog.askstring("Upload", "Enter repo name (user/repo or just repo name):")
        if not repo:
            return
        
        if "/" not in repo:
            repo = f"{acc['username']}/{repo}"
        
        self.clear_output()
        self.output(f"Uploading to {repo}...")
        
        try:
            api = GitHubAPI(acc["token"])
            if api.upload_file(repo, file_path):
                self.output("[+] File uploaded successfully!")
                messagebox.showinfo("Success", "File uploaded!")
            else:
                self.output("[x] Upload failed!")
                messagebox.showerror("Error", "Upload failed!")
        except Exception as e:
            self.output(f"[x] Error: {str(e)}")
            messagebox.showerror("Error", str(e))
    
    def create_repo_gui(self):
        acc = self.get_current_account()
        if not acc:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Create Repository")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Repository Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        desc_entry = ttk.Entry(dialog, width=30)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)
        
        private_var = tk.BooleanVar()
        ttk.Checkbutton(dialog, text="Private", variable=private_var).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        def create():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Repository name required!")
                return
            
            try:
                api = GitHubAPI(acc["token"])
                if api.create_repo(name, private_var.get(), desc_entry.get()):
                    self.output(f"[+] Repository '{name}' created!")
                    messagebox.showinfo("Success", f"Repository '{name}' created!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to create repository!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Create", command=create).grid(row=3, column=0, columnspan=2, pady=20)
    
    def run(self):
        self.root.mainloop()


def main():
    if not HAS_REQUESTS:
        print("Error: 'requests' library not found!")
        print("Install with: pip install requests")
        sys.exit(1)
    
    if not HAS_TKINTER:
        print("Error: tkinter not available!")
        print("For GUI, please install tkinter or run in terminal mode.")
        print("Install: pip install tkinter (if using pip)")
        sys.exit(1)
    
    GitHubGUI().run()


if __name__ == "__main__":
    main()