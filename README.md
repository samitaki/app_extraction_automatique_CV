```markdown
# CV Extractor

Extraction automatique d'informations depuis des CV (PDF/DOCX) par règles et regex.

## Fonctionnalités

- Upload CV (PDF ou DOCX)
- Extraction : prénom, nom, email, téléphone, diplôme
- Modification manuelle des données
- Export JSON

## Stack

**Backend** : FastAPI, pdfplumber, python-docx  
**Frontend** : Streamlit  
**Deploy** : Docker

## Structure

```
cv-extractor/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── services/
│   ├── models/
│   └── tests/
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
└── README.md
```

## Installation

```bash
git clone https://github.com/your-username/cv-extractor.git
cd cv-extractor
```

## Lancement

### Docker (recommandé)

```bash
docker compose -f docker/docker-compose.yml up --build
```

Accès :
- Frontend : http://localhost:8501
- API Swagger : http://localhost:8000/docs

Arrêter :
```bash
docker compose down
```

### Local

**Backend**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend** (nouveau terminal)
```bash
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## API

**Endpoint** : `POST /api/v1/upload-cv`

```bash
curl -X POST "http://localhost:8000/api/v1/upload-cv" \
  -F "file=@cv.pdf"
```

**Réponse**
```json
{
  "first_name": "Jean",
  "last_name": "Dupont",
  "email": "jean.dupont@example.com",
  "phone": "06 12 34 56 78",
  "degree": "Master Informatique"
}
```

## Tests

```bash
cd backend
pytest -v
```

## Notes

- Extraction par regex uniquement (pas d'IA)
- Communication Docker via variable `BACKEND_URL`
- Architecture backend/frontend découplée
```