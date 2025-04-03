# OffensiveGUI

![OffensiveGUI Logo](static/images/logo.svg)

OffensiveGUI is a web-based application designed to simplify the use of offensive security tools like Nmap. Built with Flask, it provides an intuitive interface for running network scans and managing security tasks.

---

## 🚀 Features

- **Nmap Integration**: Perform network scans directly from the web interface.
- **Responsive Design**: Built with Bootstrap 5 for a seamless experience across devices.
- **Dynamic Feedback**: Real-time feedback during scan execution.
- **Customizable Options**: Specify Nmap options and targets easily.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Tools**: Nmap, Python `nmap` library

---

## ⚙️ Installation

1. **Clone the Repository**:
    ```
    bash git clone https://github.com/yourusername/OffensiveGUI.git    
    cd OffensiveGUI
    ```

2. **Set Up a Virtual Environment:**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```
    bash pip install -r requirements.txt
    ```

4. **Run the Application:**
    ```
    bash flask run
    ```

5. **Access the Application:**
    Open your web browser and navigate to `http://127.0.0.1:8080/`.
---

## 📖 Usage

1. **Start a Scan**:
    - Enter the target IP or domain in the input field.
    - Select the desired Nmap options from the dropdown menu.
    - Click the "Start Scan" button.

2. **View Results**:
    - The scan results will be displayed in real-time on the results page.

3. **Export Results**:
    - Use the "Export" button to save the scan results as a file.

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
```