class Car:
    @staticmethod
    def get_questions():
        return [
            {"question": "Какая марка автомобиля самая популярная?", "answer": "Toyota"},
            {"question": "Как часто нужно менять масло в машине?", "answer": "Каждые 10,000 км."}
        ]


class Technology:
    @staticmethod
    def get_questions():
        return [
            {"question": "Что такое AI?", "answer": "Искусственный интеллект (AI) - это..."},
            {"question": "Что такое блокчейн?", "answer": "Блокчейн - это..."}
        ]
