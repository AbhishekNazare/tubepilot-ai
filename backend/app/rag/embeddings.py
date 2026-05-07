import hashlib
import math


class HashEmbeddingModel:
    def __init__(self, dimensions: int = 128) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in _tokens(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        return _normalize(vector)


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _tokens(text: str) -> list[str]:
    return [
        "".join(character for character in raw.lower() if character.isalnum())
        for raw in text.split()
        if raw.strip()
    ]


def _normalize(vector: list[float]) -> list[float]:
    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector
    return [value / magnitude for value in vector]

