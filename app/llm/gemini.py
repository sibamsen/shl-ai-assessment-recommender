"""
Gemini client wrapper.

Currently disabled because retrieval is used directly.
"""


class GeminiClient:

    def __init__(self, *args, **kwargs):
        pass

    def generate(self, contents):
        raise NotImplementedError(
            "Gemini is temporarily disabled."
        )