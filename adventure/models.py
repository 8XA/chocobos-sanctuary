from django.db import models

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        PASSENGERS_PER_ROW = 2
        rows_integer = self.passengers//PASSENGERS_PER_ROW
        rows_module = self.passengers%PASSENGERS_PER_ROW
        distribution_matrix = [[True for seat in range(PASSENGERS_PER_ROW)] for row in range(rows_integer)]
        if rows_module != 0:
            distribution_matrix.append([True for seat in range(rows_module)] +
                    [False for seat in range(PASSENGERS_PER_ROW - rows_module)])
        return distribution_matrix


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"


def validate_number_plate(number_plate):
    if not isinstance(number_plate, str):
        validation = False
    else:
        elements = number_plate.split('-')
        validation = len(elements) == 3 and all([
            #Three pairs validation
            len([element for element in elements if len(element) == 2]) == len(elements),
            #Only letters in the first pair validation
            elements[0].isalpha(),
            #Uppercase validation: it is a plus requirement and it can be just commented
            elements[0].isupper(),
            #Second and third pair only digits validation
            elements[1].isdigit() and elements[2].isdigit()
        ])
    return validation
