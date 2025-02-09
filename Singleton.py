import json
import os

class SingletonMeta(type):
    """Мета-класс для реализации паттерна Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Flight:
    """Класс, представляющий рейс авиакомпании."""
    
    def __init__(self, flight_number, destination, departure_time):
        self.flight_number = flight_number
        self.destination = destination
        self.departure_time = departure_time
        self.passengers = []

    def add_passenger(self, passenger):
        """Добавить пассажира в рейс."""
        self.passengers.append(passenger)

    def __repr__(self):
        return f"Рейс {self.flight_number} -> {self.destination} ({self.departure_time})"


class Passenger:
    """Класс пассажира."""
    
    def __init__(self, name, passport):
        self.name = name
        self.passport = passport

    def __repr__(self):
        return f"{self.name} ({self.passport})"


class AirportDispatcher(metaclass=SingletonMeta):
    """Класс диспетчера аэропорта (Singleton)."""
    
    def __init__(self):
        self.flights = []
        self.db_manager = DatabaseManager("result/flights.json")
        self.load_flights()

    def add_flight(self, flight):
        """Добавить рейс в систему."""
        self.flights.append(flight)
        print(f"[Диспетчер]: Добавлен {flight}")

    def list_flights(self):
        """Вывести список рейсов."""
        if not self.flights:
            print("[Диспетчер]: Нет активных рейсов.")
            return
        print("\nАктивные рейсы:")
        for flight in self.flights:
            print(f"- {flight}")

    def save_flights(self):
        """Сохранить список рейсов в JSON."""
        flights_data = [
            {"flight_number": f.flight_number, "destination": f.destination, "departure_time": f.departure_time}
            for f in self.flights
        ]
        self.db_manager.save_data(flights_data)
        print("[Диспетчер]: Рейсы сохранены в JSON.")

    def load_flights(self):
        """Загрузить рейсы из JSON."""
        flights_data = self.db_manager.load_data()
        self.flights = [Flight(f["flight_number"], f["destination"], f["departure_time"]) for f in flights_data]
        print(f"[Диспетчер]: Загружено {len(self.flights)} рейсов.")


class DatabaseManager:
    """Класс для работы с JSON-файлом."""
    
    def __init__(self, file_path):
        self.file_path = file_path

    def save_data(self, data):
        """Сохранить данные в JSON-файл."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_data(self):
        """Загрузить данные из JSON-файла."""
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)


if __name__ == "__main__":
    # === Демонстрация работы ===
    dispatcher1 = AirportDispatcher()
    dispatcher2 = AirportDispatcher()

    # Проверка, что оба диспетчера — один и тот же объект (Singleton)
    print(dispatcher1 is dispatcher2)  # True

    # Добавление рейсов
    flight1 = Flight("SU100", "Москва", "12:30")
    flight2 = Flight("BA200", "Лондон", "15:45")

    dispatcher1.add_flight(flight1)
    dispatcher1.add_flight(flight2)

    # Добавление пассажиров
    passenger1 = Passenger("Иван Петров", "123456789")
    passenger2 = Passenger("Анна Смирнова", "987654321")

    flight1.add_passenger(passenger1)
    flight2.add_passenger(passenger2)

    # Вывод списка рейсов
    dispatcher1.list_flights()

    # Сохранение рейсов
    dispatcher1.save_flights()
