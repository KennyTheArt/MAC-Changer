# 🛡️ Safe MAC Address Changer (Linux)

A modern, secure and user-friendly MAC address changer written in Python.  
It supports random or custom MAC assignment, timed rotation, MAC validation, and logging — all through a clean CLI built with `argparse`.

---

## 🚀 Features

✅ Change MAC address randomly or manually  
✅ Time-based auto MAC rotation (e.g., every X seconds/minutes/hours)  
✅ Validation with regex to prevent incorrect formats  
✅ Restore original MAC address option  
✅ Built-in interface listing support (`--list-interfaces`)  
✅ Logs all changes to `mac_change.log`  
✅ Uses modern `ip` commands instead of deprecated `ifconfig`  
✅ Fully open-source and MIT licensed

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/safe-mac-changer.git
cd safe-mac-changer
```

Make the script executable (optional):

```bash
chmod +x mac_changer.py
```

Run the script with Python 3:

```bash
python3 mac_changer.py --help
```

---

## 🛠️ Usage Examples

### 1. Randomly Change MAC Address Immediately
```bash
python3 mac_changer.py -I eth0 -M r
```

### 2. Manually Set Specific MAC Address
```bash
python3 mac_changer.py -I eth0 -M 00:11:22:33:44:55
```

### 3. Auto-Rotate MAC Address Every 10 Seconds
```bash
python3 mac_changer.py -I eth0 -M r -T 10s
```

### 4. Restore Original MAC Address
```bash
python3 mac_changer.py -I eth0 --restore
```

### 5. List All Network Interfaces
```bash
python3 mac_changer.py --list-interfaces
```

---

## ⚠️ Requirements

- Python 3.x  
- Linux OS (tested on Debian/Ubuntu-based systems)  
- `iproute2` package (for `ip` command)  
- Root privileges (`sudo`) for changing MAC address

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
You're free to use, modify, and share with proper attribution.

---

## 👨‍💻 Author

**Kanan Kenny Haji Yusifli**  
GitHub: [@KennyTheArt](https://github.com/KennyTheArt)

---

## ✨ Contribute

PRs are welcome! If you have feature requests or bug reports, open an issue or fork the repo and send a pull request.
