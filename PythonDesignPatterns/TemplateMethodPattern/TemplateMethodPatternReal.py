#! python3
from abc import abstractmethod, ABCMeta

class Trip(metaclass=ABCMeta):
    @abstractmethod
    def set_transport(self):
        pass

    @abstractmethod
    def day1(self):
        pass

    @abstractmethod
    def day2(self):
        pass

    @abstractmethod
    def day3(self):
        pass

    @abstractmethod
    def return_home(self):
        pass

    def itinerary(self):
        self.set_transport()
        self.day1()
        self.day2()
        self.day3()
        self.return_home()


class VeniceTrip(Trip):
    def set_transport(self):
        print("Take a boat.")

    def day1(self):
        print("Visit St Mark's Basilica")

    def day2(self):
        print("Enjoy the food near the Rialto Bridge")

    def day3(self):
        print("Appriciate Doge's Palace")

    def return_home(self):
        print("Get souvenirs for friends and return home.")

class MaldivesTrip(Trip):
    def set_transport(self):
        print("On foot")

    def day1(self):
        print("Enjoy the marine life of Banana Reef")

    def day2(self):
        print("Go for the water sports and snorkelling")

    def day3(self):
        print("Relax on the beach and enjoy the sun")

    def return_home(self):
        print("Don't feel like leaving the beach...")

class TravelAgency:
    def arrange_trip(self):
        choice = input("What kind of place you'd like to go to - historical or to a beach?")
        if choice == 'historical':
            self._trip = VeniceTrip()
        elif choice == 'beach':
            self._trip = MaldivesTrip()
        self._trip.itinerary()

TravelAgency().arrange_trip()
