from abc import ABC, abstractmethod

# Mediator Interface
class AirTrafficControl(ABC):
    @abstractmethod
    def notify(self, aircraft, event):
        pass

# Concrete Mediator
class TowerControl(AirTrafficControl):
    def __init__(self):
        self.aircrafts = []
        self.runway_in_use = False

    def register_aircraft(self, aircraft):
        self.aircrafts.append(aircraft)
        aircraft.set_mediator(self)

    def notify(self, aircraft, event):
        if event == "request_takeoff":
            if not self.runway_in_use:
                print(f"{aircraft.name}: Permission granted for takeoff.")
                self.runway_in_use = True
                aircraft.takeoff()
                self.runway_in_use = False
            else:
                print(f"{aircraft.name}: Runway busy. Please wait.")
        elif event == "request_landing":
            if not self.runway_in_use:
                print(f"{aircraft.name}: Permission granted for landing.")
                self.runway_in_use = True
                aircraft.land()
                self.runway_in_use = False
            else:
                print(f"{aircraft.name}: Runway busy. Please wait.")

# Colleague
class Aircraft:
    def __init__(self, name):
        self.name = name
        self.mediator = None

    def set_mediator(self, mediator):
        self.mediator = mediator

    def request_takeoff(self):
        print(f"{self.name}: Requesting permission for takeoff.")
        self.mediator.notify(self, "request_takeoff")

    def request_landing(self):
        print(f"{self.name}: Requesting permission for landing.")
        self.mediator.notify(self, "request_landing")

    def takeoff(self):
        print(f"{self.name}: Taking off!")

    def land(self):
        print(f"{self.name}: Landing!")

# Example Usage
if __name__ == "__main__":
    # Create the mediator
    tower = TowerControl()

    # Create colleagues
    aircraft1 = Aircraft("Flight A1")
    aircraft2 = Aircraft("Flight B2")
    aircraft3 = Aircraft("Flight C3")

    # Register colleagues with the mediator
    tower.register_aircraft(aircraft1)
    tower.register_aircraft(aircraft2)
    tower.register_aircraft(aircraft3)

    # Simulate events
    aircraft1.request_takeoff()
    aircraft2.request_landing()
    aircraft3.request_takeoff()
    aircraft2.request_takeoff()
