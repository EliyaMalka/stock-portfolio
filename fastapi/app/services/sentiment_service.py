from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

class SentimentService:
    """
    Singleton service responsible for performing NLP sentiment analysis.
    Uses the pre-trained FinBERT model via Hugging Face Transformers to analyze 
    financial text (like news headlines) and determine if it's positive or negative.
    """
    _instance = None

    def __new__(cls):
        """Ensures only one instance of the SentimentService (and the heavy model) is loaded."""
        if cls._instance is None:
            cls._instance = super(SentimentService, cls).__new__(cls)
            cls._instance.initialize_model()
        return cls._instance

    def initialize_model(self):
        """
        Loads the FinBERT tokenizer and sequence classification model into memory.
        Sets up the Hugging Face pipeline for sentiment analysis.
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
        Analyzes a given text string (e.g., a news headline).
        Returns a numerical sentiment score:
        - Values close to 1.0 are highly positive.
        - Values close to -1.0 are highly negative.
        - Values close to 0.0 are neutral.
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
