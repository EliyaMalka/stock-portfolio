from app.services.sentiment_service import SentimentService
import time

def test_sentiment():
    print("Initializing Sentiment Service...")
    service = SentimentService()
    
    test_cases = [
        "NVIDIA revenue skyrockets, beating all expectations.",
        "Apple faces class-action lawsuit over battery issues.",
        "The stock market remained flat today as investors wait for data."
    ]
    
    for text in test_cases:
        score = service.analyze(text)
        print(f"\nText: {text}")
        print(f"Score: {score:.4f}")
        
        if "skyrockets" in text and score < 0.5:
            print("❌ Test Failed: Positive text got low score")
        elif "lawsuit" in text and score > -0.5:
            print("❌ Test Failed: Negative text got high score")
        else:
            print("✅ Test Passed")

if __name__ == "__main__":
    test_sentiment()
