import json
import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


INDEX_FILE = "data/faiss.index"

DATA_FILE = "data/assessments.json"


print("Loading FAISS index...")


index = faiss.read_index(INDEX_FILE)


print("Loading assessments...")


with open(
    DATA_FILE,
    "r",
    encoding="utf-8"
) as f:

    assessments = json.load(f)


model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def semantic_search(query, top_k=10):

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx, distance in zip(
        indices[0],
        distances[0]
    ):

        assessment = assessments[idx]

        results.append({
            "name": assessment["name"],
            "url": assessment["url"],
            "description": (
                assessment["description"][:300]
            ),
            "distance": float(distance)
        })

    return results


if __name__ == "__main__":

    query = (
        "Java developer with "
        "stakeholder communication"
    )

    results = semantic_search(query)

    for r in results:

        print("=" * 50)

        print(f"Name: {r['name']}")

        print(f"Distance: {r['distance']}")

        print(f"URL: {r['url']}")