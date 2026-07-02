from app.retrieval.retriever import Retriever


class RecommendationService:

    def __init__(self):
        self.retriever = Retriever()

    def recommend(self, query: str):

        return self.retriever.retrieve(query)