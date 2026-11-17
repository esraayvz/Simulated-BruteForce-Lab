# Simulated Brute-Force Lab

### Project Purpose

This project is an entirely isolated educational and simulation laboratory developed to understand web-based authentication mechanisms, password hashing logic (`bcrypt`), and the working principles of **Brute-Force** attacks. It aims to comprehend the importance of security defenses by simulating real-world threat scenarios.

---

### Technologies Used

* **Python & Flask:** For the web server, routing, and backend logic.
* **HTML / Frontend:** For the user interface and data breach (`/breach`) screen.
* **Bcrypt:** For securely hashing and verifying passwords.
* **Requests (Python):** For the attacker simulation script (`attacker.py`) performing automated password attempts on the client side.
* **Custom Wordlist (`passwords.txt`):** A local wordlist containing potential passwords to be tested.

---

### Ethical, Legal, and Security Disclaimer

* **Strictly Local Environment:** This simulation is designed to run exclusively in a closed environment on the user's own computer (`127.0.0.1` - `localhost`). It is strictly not intended for any systems open to the internet, external servers, or real-world targets.
* **Fictional Data:** All credentials, names (`Alp Demir`), e-mails, and sensitive data used within the project are **entirely fictional and hypothetical**. It does not contain any real data belonging to any individual or institution.
* **Prohibition of Malicious Use:** The purpose of the project is entirely to gain cybersecurity awareness and learn how to secure software architectures. The code cannot be used for malicious purposes; any liability arising from misuse rests solely with the user implementing it.
