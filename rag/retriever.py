import os
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


KNOWLEDGE_BASE_DIR = "knowledge_base"

# Documents below this similarity are treated as
# not relevant enough for the user's question.
MIN_SIMILARITY = 0.05


def load_documents() -> List[Dict[str, str]]:
    """
    Load all text documents from the knowledge base.
    """

    documents = []

    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        return documents

    for filename in os.listdir(KNOWLEDGE_BASE_DIR):

        if not filename.endswith(".txt"):
            continue

        path = os.path.join(
            KNOWLEDGE_BASE_DIR,
            filename
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        documents.append(
            {
                "source": filename,
                "content": content,
            }
        )

    return documents


def retrieve_documents(
    query: str,
    top_k: int = 2,
) -> List[Dict[str, str]]:
    """
    Retrieve the most relevant knowledge-base documents.

    TF-IDF converts documents and the query into vectors.
    Cosine similarity measures how relevant each document
    is to the query.
    """

    documents = load_documents()

    if not documents:
        return []

    texts = [
        document["content"]
        for document in documents
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    document_vectors = vectorizer.fit_transform(
        texts
    )

    query_vector = vectorizer.transform(
        [query]
    )

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    ranked_indices = similarities.argsort()[::-1]

    results = []

    for index in ranked_indices:

        score = float(
            similarities[index]
        )

        if score < MIN_SIMILARITY:
            continue

        results.append(
            {
                "source": documents[index]["source"],
                "content": documents[index]["content"],
                "score": score,
            }
        )

        if len(results) >= top_k:
            break

    return results


def build_context(
    results: List[Dict[str, str]]
) -> str:
    """
    Convert retrieved documents into context
    for the LLM.
    """

    if not results:

        return (
            "No sufficiently relevant knowledge-base "
            "information was found. "
            "Answer using the provided resume and "
            "job description only."
        )

    context_parts = []

    for result in results:

        context_parts.append(
            f"SOURCE: {result['source']}\n"
            f"{result['content']}"
        )

    return "\n\n----------------------\n\n".join(
        context_parts
    )