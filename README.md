# EmoChat.ai
EmoChat is an intelligent and empathetic mental health chatbot designed to provide a safe and supportive space for users. Fine-tuned for handling sensitive conversations, EmoChat delivers fast, accurate, and human-like responses, leveraging a private, local AI model to ensure user data never leaves their machine.
### :hammer_and_wrench: Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![LM Studio](https://img.shields.io/badge/LM_Studio-000000?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEyIDJDNi40ODQgMiAyIDYuNDg0IDIgMTJzNC40ODQgMTAgMTAgMTAgMTAtNC40ODQgMTAtMTBTMTcuNTE2IDIgMTIgMnptMCAxOGMtNC40MTEgMC04LTMuNTg5LTgtOHMzLjU4OS04IDgtOCA4IDMuNTg5IDggOC0zLjU4OSA4LTggOHoiIGZpbGw9IiNmZmYiIGNsYXNzPSJmaWxsLTAwMDAwMCI+PC9wYXRoPjxwYXRoIGQ9Ik0xMiA3Yy0yLjc1OCAwLTUgMi4yNDItNSA1czIuMjQyIDUgNSA1IDUtMi4yNDIgNS01LTIuMjQyLTUtNS01em0wIDhjLTEuNjU0IDAtMy0xLjM0Ni0zLTNzMS4zNDYtMyAzLTMgMyAxLjM0NiAzIDMtMS4zNDYgMy0zIDN6IiBmaWxsPSIjZmZmIiBjbGFzcz0iZmlsbC0wMDAwMDAiPjwvcGF0aD48L3N2Zz4=) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
---
### :zap: Quick Setup
**1. Clone the repo**
```bash
git clone https://github.com/NizzCorp-Academy/EmoChat.git
```
**2. Install dependencies**
```bash
pip install -r requirements.txt
```
**3. Set up the `.env` file**
Create a `.env` file in the project root and add the following variables:
```env
# Database Configuration
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=mindmate_db
# LM Studio API
LM_STUDIO_API_URL=http://localhost:1234/v1
# Streamlit App Secret Key
SECRET_KEY=your_super_secret_key_for_sessions
```
**4. Initialize the database**
Make sure your MySQL server is running, then run the setup script:
```bash
python -m db.init_db
```
**5. Running the app**
```bash
streamlit run ui/app.py
```
### :books: Documentation
To view the project documentation, open the `docs/index.html` file in your web browser, or run the following command from the project root:
```bash
start docs/index.html
```
### :busts_in_silhouette: TEAM MEMBERS
- Arshad Ibrahim ([@arshad-v](https://github.com/arshad-v))
- Shuaib Backer ([@shuaibbacker](https://github.com/shuaibbacker))
- Adhil .T ([@adiltkt](https://github.com/adiltkt))
---
### :male-teacher: Acknowledgements
- Ujwal ([@UjwalNizzCorp](https://github.com/UjwalNizzCorp))
---
### :page_facing_up: License & Usage
All projects in this repository are intended for educational and demonstration purposes only. Use or reuse of any code, design, or documentation must be done with proper attribution.
Please respect the intellectual efforts of all contributors.
---







