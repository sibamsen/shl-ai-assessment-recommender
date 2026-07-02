class MetadataFilter:

    def filter(self, items, top_k=10):

        seen = set()

        final = []

        for item in items:

            if item["entity_id"] in seen:
                continue

            seen.add(item["entity_id"])

            final.append(item)

            if len(final) == top_k:
                break

        return final