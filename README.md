# OffensiveGUI

![OffensiveGUI Logo](static/images/logo.svg)

OffensiveGUI is a web-based application designed to simplify the use of offensive security tools like Nmap. Built with Flask, it provides an intuitive interface for running network scans, managing targets, monitoring their status, and logging actions.

---

## 🚀 Features

- **Nmap Integration**: Perform various types of network scans (TCP, UDP, Xmas, Service, OS) directly from the web interface.
- **Target Management**: Add, edit, and delete targets easily.
- **Action Logging**: View a history of actions performed on targets.
- **Target Monitoring**: Monitor the online/offline status of targets in real-time.
- **Database Management**: Delete or recreate the database directly from the settings page.
- **Responsive Design**: Built with Bootstrap 5 for a seamless experience across devices.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Database**: SQLite (with SQLAlchemy ORM)
- **Tools**: Nmap, Python `nmap` library

---

## ⚙️ Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/jensbecker-dev/OffensiveGUI.git    
    cd OffensiveGUI
    ```

2. **Set Up a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application:**
    ```bash
    python app.py
    ```

    **or**

    ```bash
    flask run --port=8080
    ```

5. **Access the Application:**

    Open your web browser and navigate to `http://127.0.0.1:8080/`.

---

## 📖 Usage

### Dashboard
- View an overview of targets, their statuses, and recent actions.
- Monitor the online/offline status of targets in real-time.

### Nmap Scans
- Select a target and perform various types of scans:
  - **TCP Scan**
  - **UDP Scan**
  - **Xmas Scan**
  - **Service Scan**
  - **OS Scan**
- View detailed scan results.

### Target Management
- Add new targets to the database.
- Edit or delete existing targets.

### Settings
- **Delete Database**: Permanently delete all data in the database.
- **Recreate Database**: Recreate the database structure, clearing all existing data.

---

## 🖼️ Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Nmap Scans

![Nmap Scans](screenshots/nmap.png)

### Settings

![alt text](screenshots/settings.png)

### Targets

![alt text](screenshots/targets.png)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
