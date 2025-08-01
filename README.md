# EmoChat

EmoChat is an intelligent and empathetic mental health chatbot designed to provide a safe and supportive space for users. Fine-tuned for handling sensitive conversations, EmoChat delivers fast, accurate, and human-like responses, leveraging a private, local AI model to ensure user data never leaves their machine.

### :hammer_and_wrench: TECH STACK

| Category   | Technology                                       |
|------------|--------------------------------------------------|
| Frontend   | [Streamlit](https://streamlit.io/)               |
| Backend    | [Python](https://www.python.org/)                |
| DataBase   | [MySQL](https://www.mysql.com/)                  |
| Model      | Fine-tuned GGUF Model (via LM Studio)            |
| Deployment | [Docker](https://www.docker.com/) (Planned)      |
---
### :zap: Quick Setup
**1. Clone the repo**
```bash
git clone https://github.com/NizzCorp-Academy/EmoChat.git
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
python -m mindmate.db.init_db
```
**5. Running the app**
```bash
streamlit run mindmate/ui/app.py
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
