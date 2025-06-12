# 🌌 AstroLogger

AstroLogger is a lightweight, dark-themed astronomy observation log built with Python and Tkinter. Designed for both amateur stargazers and seasoned astronomers, it allows you to easily document and manage your celestial observations in a clean, GUI-based interface.

## ✨ Features
* 📝 Log observation details: Date/Time, Weather, Target,   Classification, Specifications, and Notes

* 🖼️ Attach and preview observation images (e.g., telescope captures)

* 💾 Save, view, edit, and delete past logs

* 🔍 Organized tabbed interface: Current Log and Stored Logs

* 🌑 Dark mode optimized for night-time use

* ♻️ Reset form with a single click

## 📁 Log Format

Logs are stored in a simple logs.json file with the following structure:

```json
{
  "Time/Date": "2025-06-11 22:00",
  "Weather": "Clear",
  "Target": "Saturn",
  "Class": "Planet",
  "Specs": "8\" Dobsonian, 25mm eyepiece",
  "Notes": "Excellent seeing, Cassini Division visible.",
  "Image": "C:/images/saturn_2025.jpg"
}
```
## 🧰 Tech Stack

- Python 3.8+
- Tkinter (GUI)
- PIL (Pillow) for image handling
- JSON for persistent storage

## 🛠️ Installation
1. Clone the repo

```bash
git clone https://github.com/yourusername/AstroLogger.git
cd AstroLogger
```

2. Install dependencies

```bash
pip install pillow
```
3. Run the app

```bash
python AstroLogger.py
```
## 🧠 Use Case
Whether you're tracking deep sky objects, planets, comets, or the moon — AstroLogger helps you stay organized, visualize your logs, and build a digital history of your night sky adventures.

## 📜 License
This project is licensed under the Apache 2.0 License.

## 🤝 Contributions
Contributions are welcome! Open a pull request, suggest features, or report bugs via Issues.

## 📬 Contact
For any questions or suggestions: elishahjohn9@gmail.com
