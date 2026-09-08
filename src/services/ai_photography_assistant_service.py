class AIPhotographyAssistantService:

    def __init__(self, knowledge_repository):
        self.knowledge_repository = knowledge_repository

    def ask(self, question):
        knowledge_list = self.knowledge_repository.list_all()

        question_words = set(
            question.lower().split()
        )

        results = []

        for knowledge in knowledge_list:
            if knowledge.status != "published":
                continue

            title = knowledge.title or ""
            content = knowledge.content or ""

            text = f"{title} {content}".lower()

            score = 0

            for word in question_words:
                if len(word) < 2:
                    continue

                if word in text:
                    score += 1

            if score > 0:
                results.append({
                    "knowledge": knowledge,
                    "score": score
                })

        results.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        top_results = results[:3]

        if not top_results:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the photography knowledge base."
                ),
                "sources": []
            }

        answer_parts = []

        for item in top_results:
            knowledge = item["knowledge"]

            answer_parts.append(
                f"{knowledge.title}: {knowledge.content}"
            )

        return {
            "answer": "\n\n".join(answer_parts),
            "sources": [
                {
                    "id": str(item["knowledge"].id),
                    "title": item["knowledge"].title
                }
                for item in top_results
            ]
        }