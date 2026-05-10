import json
import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


DATA_FILE = "data/assessments.json"

INDEX_FILE = "data/faiss.index"

MAPPING_FILE = "data/id_mapping.json"


print("Loading assessments...")


with open(
    DATA_FILE,
    "r",
    encoding="utf-8"
) as f:

    assessments = json.load(f)


print(f"Loaded {len(assessments)} assessments")


model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


documents = []

id_mapping = []


for idx, assessment in enumerate(assessments):

    combined_text = " ".join([
        assessment.get("name", ""),
        assessment.get("description", ""),
        " ".join(
            assessment.get("keywords", [])
        )
    ])

    documents.append(combined_text)

    id_mapping.append({
        "id": idx,
        "name": assessment.get("name"),
        "url": assessment.get("url")
    })


print("Generating embeddings...")


embeddings = model.encode(
    documents,
    show_progress_bar=True
)


embeddings = np.array(
    embeddings
).astype("float32")


dimension = embeddings.shape[1]


print(f"Embedding dimension: {dimension}")


index = faiss.IndexFlatL2(dimension)


index.add(embeddings)


print(
    f"FAISS index built with "
    f"{index.ntotal} vectors"
)


faiss.write_index(
    index,
    INDEX_FILE
)


with open(
    MAPPING_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        id_mapping,
        f,
        indent=2,
        ensure_ascii=False
    )


print("Index saved successfully.")