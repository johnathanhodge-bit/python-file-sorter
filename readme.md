# Personal Automation: Local File Organizer
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Purpose
This is a Python-based utility designed to automate directory hygiene. It demonstrates a "Logic-from-Policy" architecture, where the sorting rules are decoupled from the execution engine for maximum flexibility and security.

## 🛠️ Tech Stack
- **Language:** Python 3.12+
- **Configuration:** JSON-driven policy management
- **Interface:** Tkinter GUI (Native)
- **Logging:** Integrated audit trail (`organizer.log`)

## 🔐 Key Features
- **Zero Cloud Footprint:** All operations occur locally on your machine.
- **Dynamic Rules:** Modify `config.json` to add new file categories without changing a single line of code.
- **Error Resilience:** Gracefully handles permission issues and system-protected files.
- **Audit Trail:** Every file movement is timestamped and recorded for transparency.

## 🚀 How to Use
1. **Initialize:** Ensure you have Python installed.
2. **Configure:** Edit `config.json` to define your desired folder names and file extensions.
3. **Execute:** Run `python3 organizer.py`.
4. **Select:** Use the visual dialog to pick the folder you wish to organize.

---
*Developed as a proof-of-concept for AI-assisted executive automation.*