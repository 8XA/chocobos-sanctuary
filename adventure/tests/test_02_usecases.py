import pytest
from datetime import date
from django.utils import timezone

from adventure import models, notifiers, repositories, usecases

#########
# Mocks #
#########


@pytest.fixture
def car():
    return models.VehicleType(max_capacity=4)


@pytest.fixture
def tesla(car):
    return models.Vehicle(
        name="Tesla", passengers=3, vehicle_type=car, number_plate="AA-12-34"
    )


class MockJourneyRepository(repositories.JourneyRepository):
    def get_or_create_car(self) -> models.VehicleType:
        return models.VehicleType(name="car", max_capacity=4)

    def create_vehicle(
        self, name: str, passengers: int, vehicle_type: models.VehicleType
    ) -> models.Vehicle:
        return models.Vehicle(
            name=name, passengers=passengers, vehicle_type=vehicle_type
        )

    def create_journey(self, vehicle) -> models.Journey:
        return models.Journey(vehicle=vehicle, start=timezone.now().date())


class MockNotifier(notifiers.Notifier):
    def send_notifications(self, journey: models.Journey) -> None:
        pass


#########
# Tests #
#########


class TestStartJourney:
    def test_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 2}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        journey = usecase.execute()

        assert journey.vehicle.name == "Kitt"

    def test_cant_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 6}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        with pytest.raises(usecases.StartJourney.CantStart):
            journey = usecase.execute()


class TestStopJourney:
    #@pytest.mark.skip  # Remove
    def test_stop(self, tesla):
        # TODO: Implement a StopJourney Usecase
        # it takes a started journey as a parameter and sets an "end" value
        # then saves it to the database

        #Journey created
        journey = models.Journey(start=date.today(), vehicle=tesla)
        #Verifies the journey is not finished
        assert not journey.is_finished()
        #Finishes the journey
        usecases.StopJourney(journey, end_date=date.today())
        #Verifies the journey is finished
        assert journey.is_finished()
