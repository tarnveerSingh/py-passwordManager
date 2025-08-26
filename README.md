# 🔐 Python Password Manager

A simple and secure **command-line password manager** built with **Python**.  
It uses **SQLite** for local storage and **Fernet encryption** from the `cryptography` library to keep your passwords safe.

---

## ✨ Features

- ✅ Save new passwords (encrypted before storage)  
- ✅ View all saved passwords (optionally decrypted)  
- ✅ Delete passwords by service & username  
- ✅ Secure encryption with **Fernet (symmetric encryption)**  
- ✅ Lightweight: only Python + SQLite, no external DB required  

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **SQLite3** (built-in database)
- **cryptography (Fernet)** for password encryption & decryption

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/tarnveerSingh/py-passwordManager.git
cd py-passwordManager

pip install dot-env cryptography
