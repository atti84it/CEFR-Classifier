r"""
Sample script that shows how to use CEFRClassifier
"""

from cefr_classifier import CEFRClassifier

def main():
    classifier = CEFRClassifier()
    
    sample_text = "Hai voglia di giocare al computer con noi?"
    result = classifier.classify(sample_text)
    
    print(f"The CEFR level of the text is: {result}")

if __name__ == "__main__":
    main()