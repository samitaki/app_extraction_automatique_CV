from fastapi import FastAPI, UploadFile, File, HTTPException
from services.pdf_parser import parse_pdf
from services.docx_parser import parse_docx
from services.extractor import Extractor
from models.cv_result import CvResult

extractor = Extractor()
app = FastAPI()

@app.post("/api/v1/upload-cv", response_model=CvResult)
async def upload_cv(file: UploadFile = File(...)):
    # Vérifier que c'est bien un PDF ou DOCX
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF ou un DOCX.")
    
    # Lire le contenu du fichier
    content = await file.read()
    
    # Extraire le texte en fonction du type de fichier
    if file.filename.endswith('.pdf'):
        text = parse_pdf(content)
    elif file.filename.endswith('.docx'):
        text = parse_docx(content)
    
    # Normaliser le texte extrait
    cleaned_text = extractor.normalize_text(text)
    
    # Extraire les informations (email, téléphone, etc.)
    result = extractor.extract_all(cleaned_text)
    
    # Retourner le résultat au frontend
    return result
