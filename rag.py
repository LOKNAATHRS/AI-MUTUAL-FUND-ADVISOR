import os
 
def load_documents():
 
    path = os.path.join("data", "mutual_funds.txt")
 
    with open(path, "r", encoding="utf-8") as f:
        docs = f.readlines()
 
    return docs
 
 
# Fix: filter out common stopwords so short/generic words don't match
# irrelevant lines in the document store
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "what", "how", "why", "when", "where", "which", "who",
    "i", "in", "of", "to", "for", "on", "at", "by", "with",
    "and", "or", "but", "if", "my", "me", "do", "can", "should"
}
 
def retrieve_context(query, docs):
 
    keywords = [
        word.lower()
        for word in query.split()
        if word.lower() not in STOPWORDS and len(word) > 2
    ]
 
    # If all words were stopwords, fall back to the original behaviour
    if not keywords:
        keywords = [word.lower() for word in query.split()]
 
    results = []
 
    for doc in docs:
        if any(keyword in doc.lower() for keyword in keywords):
            results.append(doc)
 
    return " ".join(results[:3])
 