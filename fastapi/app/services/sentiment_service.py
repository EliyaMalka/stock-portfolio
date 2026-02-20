from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

class SentimentService:
    """
    שירות סינגלטון האחראי על ביצוע ניתוח סנטימנט ב-NLP.
    משתמש במודל FinBERT מאומן מראש דרך Hugging Face Transformers לניתוח
    טקסט פיננסי (כמו כותרות חדשות) ולקבוע אם הוא חיובי או שלילי.
    """
    _instance = None

    def __new__(cls):
        """מבטיח שרק מופע אחד של SentimentService (והמודל הכבד) ייטען."""
        if cls._instance is None:
            cls._instance = super(SentimentService, cls).__new__(cls)
            cls._instance.initialize_model()
        return cls._instance

    def initialize_model(self):
        """
        טוען את המטוקן (tokenizer) ומודל סיווג הרצפים של FinBERT לזיכרון.
        מגדיר את ה-pipeline של Hugging Face לניתוח סנטימנט.
        """
        print("Loading FinBERT model... This may take a while using CPU.")
        self.model_name = "ProsusAI/finbert"
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.analyzer = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
            print("FinBERT model loaded successfully.")
        except Exception as e:
            print(f"Failed to load FinBERT: {e}")
            self.analyzer = None

    def analyze(self, text: str) -> float:
        """
        מנתח מחרוזת טקסט נתונה (לדוגמה, כותרת חדשות).
        מחזיר ציון סנטימנט מספרי:
        - ערכים קרובים ל-1.0 הם חיוביים מאוד.
        - ערכים קרובים ל- -1.0 הם שליליים מאוד.
        - ערכים קרובים ל-0.0 הם ניטרליים.
        """
        if not self.analyzer:
            return 0.0

        try:
            # FinBERT returns: [{'label': 'positive', 'score': 0.95}]
            # Labels can be: 'positive', 'negative', 'neutral'
            result = self.analyzer(text)[0]
            
            raw_score = result['score']
            label = result['label']

            if label == 'positive':
                return raw_score
            elif label == 'negative':
                return -raw_score
            else: # neutral
                return 0.0
                
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return 0.0
