import datetime


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


class Chelyabinsk:
    @staticmethod
    def get_questions():
        return [
                {"question": "Сколько лет Челябинску?", "answer": f"Челябинску {datetime.now().year - 1736} лет."},
                {"question": "Когда был основан Челябинск?", "answer": "Челябинск был основан в 1736 году."}
            ]


class nVidia:
    @staticmethod
    def get_questions():
        return [
            {"question": "Что такое nVidia?", "answer": "Nvidia — это американская компания, ведущий мировой производитель высокопроизводительных графических процессоров (GPU) и систем-на-чипе (SoC), а также программного обеспечения."},
            {"question": "Какой самый популярный продукт у Nvidia?", "answer": "Как сообщает Bloomberg, самым популярным технологическим продуктом уходящего года стал AI-ускоритель NVIDIA H100."}
        ]
