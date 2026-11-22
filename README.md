# Sorry page (Achal → Priyanka)

## 1. GitHub par upload
GitHub par new repository banao, phir "Add file → Upload files" se ye 4 files daalo:
`app.py`, `index.html`, `requirements.txt`, `README.md` → Commit.

## 2. Render par deploy
New → Web Service → apni GitHub repo chuno.
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --workers 1`
- Environment variable: `ADMIN_KEY` = koi lamba secret word (jaise `achal-secret-2026`)

## 3. Dekhna
- Priyanka ko Render ka link bhejo (`https://xxxx.onrender.com`).
- Kya kya dabaya (flowers / chai date / chocolate, sign, hug...) yahan dikhega:
  `https://xxxx.onrender.com/admin?key=TUMHARA_ADMIN_KEY`

Note: Render free plan 15 min idle rehne par so jata hai, pehla load ~50 sec le sakta hai.
Bhejne se 5 min pehle link khud khol lo. Free plan restart/redeploy par purani list mit sakti hai.
