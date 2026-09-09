import os
import re
import unicodedata
from difflib import SequenceMatcher


class AIPhotographyAssistantService:
    def __init__(self, knowledge_repository=None):
        # Giữ tham số này để không phải sửa controller.
        self.knowledge_repository = knowledge_repository

        self.knowledge_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "infrastructure",
            "databases",
            "photography_knowledge.txt",
        )

        self.knowledge_data = self._load_knowledge()

    # ============================================================
    # LOAD DATA FROM TXT
    # ============================================================

    def _load_knowledge(self):
        if not os.path.exists(self.knowledge_file):
            return []

        try:
            with open(
                self.knowledge_file,
                "r",
                encoding="utf-8"
            ) as file:
                lines = [line.strip() for line in file.readlines()]
        except Exception:
            return []

        knowledge = []

        i = 0

        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            # Chỉ coi dòng là câu hỏi nếu:
            # - Viết hoa
            # - Có dấu ?
            if not self._is_question_title(line):
                i += 1
                continue

            question = line

            # Tìm phần trả lời ngay phía sau câu hỏi
            answer_lines = []
            j = i + 1

            while j < len(lines):
                current = lines[j].strip()

                if not current:
                    break

                # Nếu gặp một câu hỏi mới thì dừng
                if self._is_question_title(current):
                    break

                answer_lines.append(current)
                j += 1

            answer = " ".join(answer_lines).strip()

            if answer:
                knowledge.append({
                    "id": str(len(knowledge) + 1),
                    "question": question,
                    "answer": answer,
                })

            i = max(j, i + 1)

        return knowledge

    # ============================================================
    # QUESTION DETECTION
    # ============================================================

    def _is_question_title(self, text):
        if not text:
            return False

        if "?" not in text:
            return False

        # Các dòng metadata đầu file sẽ không được coi là câu hỏi
        metadata = [
            "FILMLAB PHOTOGRAPHY KNOWLEDGE TEST",
            "1000 QUESTIONS AND ANSWERS",
            "TEMPORARY TEST KNOWLEDGE BASE",
        ]

        upper_text = text.upper()

        if upper_text in metadata:
            return False

        # Dataset câu hỏi của chúng ta là uppercase
        return text == text.upper()

    # ============================================================
    # NORMALIZE VIETNAMESE
    # ============================================================

    def _normalize(self, text):
        if not text:
            return ""

        text = text.lower().strip()

        # Bỏ dấu tiếng Việt để:
        # "khi nào" và "khi nao"
        # vẫn được coi là giống nhau.
        text = unicodedata.normalize("NFD", text)

        text = "".join(
            char
            for char in text
            if unicodedata.category(char) != "Mn"
        )

        text = text.replace("đ", "d")

        # Chỉ giữ chữ và số
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        # Gom nhiều khoảng trắng
        text = re.sub(r"\s+", " ", text).strip()

        return text

    # ============================================================
    # REMOVE COMMON WORDS
    # ============================================================

    def _get_keywords(self, text):
        normalized = self._normalize(text)

        words = normalized.split()

        stop_words = {
            "la",
            "gi",
            "thi",
            "co",
            "the",
            "nao",
            "khi",
            "nhi",
            "cho",
            "mot",
            "cua",
            "va",
            "hay",
            "de",
            "duoc",
            "voi",
            "trong",
            "tren",
            "tu",
            "den",
            "can",
            "nen",
            "se",
            "bi",
            "o",
            "anh",
            "toi",
            "minh",
            "ban",
        }

        return {
            word
            for word in words
            if len(word) >= 2 and word not in stop_words
        }

    # ============================================================
    # CALCULATE SIMILARITY
    # ============================================================

    def _calculate_score(self, user_question, knowledge_question):
        user_normalized = self._normalize(user_question)
        knowledge_normalized = self._normalize(knowledge_question)

        if not user_normalized or not knowledge_normalized:
            return 0.0

        # --------------------------------------------------------
        # 1. Exact match
        # --------------------------------------------------------

        if user_normalized == knowledge_normalized:
            return 1.0

        # --------------------------------------------------------
        # 2. Character similarity
        # --------------------------------------------------------

        sequence_score = SequenceMatcher(
            None,
            user_normalized,
            knowledge_normalized
        ).ratio()

        # --------------------------------------------------------
        # 3. Keyword similarity
        # --------------------------------------------------------

        user_keywords = self._get_keywords(user_question)
        knowledge_keywords = self._get_keywords(knowledge_question)

        if not user_keywords or not knowledge_keywords:
            keyword_score = 0.0
        else:
            intersection = user_keywords.intersection(
                knowledge_keywords
            )

            union = user_keywords.union(
                knowledge_keywords
            )

            keyword_score = (
                len(intersection) / len(union)
                if union
                else 0.0
            )

        # --------------------------------------------------------
        # 4. Keyword containment
        # --------------------------------------------------------

        containment_score = 0.0

        if user_keywords and knowledge_keywords:
            matched = 0

            for word in user_keywords:
                if word in knowledge_keywords:
                    matched += 1
                    continue

                # Cho phép câu hỏi người dùng viết dài hơn
                # hoặc dùng biến thể gần giống.
                for knowledge_word in knowledge_keywords:
                    if (
                        len(word) >= 4
                        and len(knowledge_word) >= 4
                        and (
                            word in knowledge_word
                            or knowledge_word in word
                        )
                    ):
                        matched += 1
                        break

            containment_score = matched / len(user_keywords)

        # --------------------------------------------------------
        # Final score
        # --------------------------------------------------------

        score = (
            sequence_score * 0.45
            + keyword_score * 0.35
            + containment_score * 0.20
        )

        return score

    # ============================================================
    # FIND BEST QUESTION
    # ============================================================

    def _find_best_match(self, question):
        if not self.knowledge_data:
            return None, 0.0

        best_item = None
        best_score = 0.0

        for item in self.knowledge_data:
            score = self._calculate_score(
                question,
                item["question"]
            )

            if score > best_score:
                best_score = score
                best_item = item

        return best_item, best_score

    # ============================================================
    # ASK AI
    # ============================================================

    def ask(self, question):
        question = (question or "").strip()

        if not question:
            return {
                "answer": "Vui lòng nhập câu hỏi.",
                "sources": []
            }

        best_item, best_score = self._find_best_match(question)

        # Không có dữ liệu
        if not best_item:
            return {
                "answer": (
                    "Xin lỗi, hiện tại tôi không tìm thấy "
                    "thông tin phù hợp trong kho kiến thức."
                ),
                "sources": []
            }

        # Ngưỡng để tránh trả lời một câu hoàn toàn không liên quan.
        #
        # Nếu điểm quá thấp thì không trả lời bừa.
        if best_score < 0.30:
            return {
                "answer": (
                    "Xin lỗi, hiện tại tôi không tìm thấy "
                    "thông tin phù hợp với câu hỏi của bạn."
                ),
                "sources": []
            }

        # Chỉ trả về đúng 1 câu trả lời phù hợp nhất.
        return {
            "answer": best_item["answer"],
            "sources": [
                {
                    "id": best_item["id"],
                    "title": best_item["question"],
                    "score": round(best_score, 3)
                }
            ]
        }