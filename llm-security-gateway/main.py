from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import time

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

patterns = {
    "ignore previous instructions": 0.4,
    "reveal system prompt": 0.5,
    "developer mode": 0.4,
    "bypass safety": 0.4
}

def detect_injection(text):
    score = 0
    text = text.lower()

    for p in patterns:
        if p in text:
            score += patterns[p]

    return score


def gateway(text):

    start = time.time()

    injection_score = detect_injection(text)

    pii_results = analyzer.analyze(text=text, language="en")

    if injection_score > 0.6:
        return "BLOCKED: Prompt Injection Detected"

    if len(pii_results) > 0:
        anonymized = anonymizer.anonymize(text=text, analyzer_results=pii_results)
        return anonymized.text

    end = time.time()

    latency = (end-start)*1000

    return f"SAFE INPUT (Latency {latency:.2f} ms): {text}"


while True:
    user_input = input("Enter text: ")
    print(gateway(user_input))