"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "730434819"  # TODO


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, obj: Point) -> float:
        """Calculate the distance between two points."""
        dis = sqrt((obj.x - self.x) ** 2 + (obj.y - self.y) ** 2)
        return dis


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.
    def tick(self) -> None:
        """Update the state of a cell's object."""
        self.location = self.location.add(self.direction)
        if self.is_infected():
            self.sickness += 1
        if self.sickness > constants.RECOVERY_PERIOD:
            self.immunize()

    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_infected():
            return "red"
        if self.is_immune():
            return "cornflower blue"
        else:
            return "gray"

    def contract_disease(self) -> None:
        """Assign the INFECTED constant to the sickness attribute."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Whether the cell's sickness is equal to VULNERABLE."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False
    
    def is_infected(self) -> bool:
        """Whether the cell's sickness is equal to INFECTED."""
        if self.sickness >= constants.INFECTED:
            return True
        else:
            return False

    def contact_with(self, contactor: Cell) -> None:
        """Check whether one of the cell is infected."""
        if contactor.is_infected() and self.is_vulnerable():
            self.contract_disease()

        if contactor.is_vulnerable() and self.is_infected():
            contactor.contract_disease()
    
    def immunize(self) -> None:
        """Assign IMMUNE to the sickness."""
        self.sickness = constants.IMMUNE
    
    def is_immune(self) -> bool:
        """Check whether the cell is immunize to the disease."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False


class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, infected_num: int, immune_num: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        if infected_num >= cells or infected_num <= 0:
            raise ValueError("Some number of the Cell objecte must begin with infected.")

        if immune_num > cells or immune_num < 0:
            raise ValueError("Improper number of immune cell.")

        for _ in range(0, cells):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
             
        temp: int = 0
        for i in range(0, infected_num):
            self.population[i].contract_disease()
            temp += 1
        
        for j in range(0, immune_num):
            self.population[j + temp].immunize()
    
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.check_contacts()
            self.enforce_bounds(cell)

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        x_dir = cos(random_angle) * speed
        y_dir = sin(random_angle) * speed
        return Point(x_dir, y_dir)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def check_contacts(self) -> None:
        """Check whether any two Cell values come in "contact"."""
        for i in range(0, len(self.population)):
            for j in range(i + 1, len(self.population)):
                if self.population[i].location.distance(self.population[j].location) < float(constants.CELL_RADIUS):
                    self.population[i].contact_with(self.population[j])

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        for cell in self.population:
            if cell.is_infected():
                return False
        return True