import re
from pydantic import BaseModel
from models.cv_result import CVResult

## Variables globales
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}") # email regex 
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{1,4}\)?[\s.-]?)?(?:\d[\d\s.-]{5,}\d)") ## phone number
DEGREE_KEYWORDS = ["master", "licence", "bachelor", "ingenieur", "ingénieur", "doctorat", "phd", "msc", "bsc", "diplôme"] # liste des mots-clés possibles pour les diplômes

class Extractor(BaseModel):
    result = CVResult()

    def extract_email(self, text: str):
        m = EMAIL_RE.search(text)
        if m:
            self.result.email = m.group(0)
    
    def extract_phone(self, text: str):
        m = PHONE_RE.search(text)
        if m:
            self.result.phone = m.group(0)
    

    def extract_degree(self, text:str):
        lower = text.lower()
        for kw in DEGREE_KEYWORDS:
            if kw in lower:
                # retourner la ligne contenant le mot-clé
                for ln in text.splitlines():
                    if kw in ln.lower():
                        self.result.degree = ln.strip()
                        return

    def extract_name(self, first_page: str):
        for line in first_page.splitlines():
            L = line.strip()
            if not L:
                continue
            if EMAIL_RE.search(L) or PHONE_RE.search(L):
                continue
            # accept if 2-3 words and letters (simple)
            parts = [p for p in L.split() if any(c.isalpha() for c in p)]
            if 1 < len(parts) <= 3: ## On suppose que la longueur maximale d'un nom complet est de 3 mots
                if(len(parts) > 2):
                    self.result.first_name = parts[0]
                    self.result.last_name = " ".join(parts[1:])
                else: 
                    self.result.first_name = parts[0]       
                    self.result.last_name = parts[1]
                return   
            
    def extract_all(self, full_text: str):

        normalized = normalize_text(full_text)
        text_flat = normalized.replace("\n", " ")
        first_page = "\n".join(full_text.splitlines()[:10])

        ## Pour email et phone, on utilise le texte aplati (sans sauts de ligne)
        self.extract_email(text_flat)
        self.extract_phone(text_flat)

        ## Pour le diplôme et le nom, on utilise le texte complet avec sauts de ligne
        self.extract_degree(full_text)
        self.extract_name(first_page)
        return self.result
    

### fonction de normalisation du texte
import unidecode

def normalize_text(text: str) -> str:
    text = text.lower()
    text = " ".join(text.split())
    text = unidecode.unidecode(text)
    
    return text
