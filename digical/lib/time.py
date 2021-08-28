from __future__ import annotations
from functools import total_ordering
from typing import Union


@total_ordering
class Time:
    _weekdays = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

    def __init__(self, value: int):
        """Time(int) -> Time"""
        self._value = value

    @classmethod
    def from_dhm(cls, day: int, hour: int, minutes: int) -> Time:
        """Time.from_dhm(int, int, int) -> Time"""
        value = minutes + (hour * 60) + (day * 60 * 24)
        return cls(value)

    @classmethod
    def from_json(cls, j: dict) -> Time:
        """Time.from_json(dict) -> Time"""
        return cls(j["value"])

    def to_json(self) -> dict:
        """Time.to_json() -> dict"""
        return {"value": self._value}

    def copy(self):
        """Time.copy() -> Time"""
        return Time(self._value)

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        """repr(Time) -> str"""
        return f"Time({self._value})"

    def __str__(self) -> str:
        """str(Time) -> str"""
        return f"{self.dayname}, {self.hour}:{self.minute:02}"

    @property
    def value(self) -> int:
        """Time.value -> int"""
        return self._value

    @property
    def weekday(self) -> int:
        """Time.weekday -> int"""
        return self.day % 7

    @property
    def day(self) -> int:
        """Time.day -> int"""
        return self._value // (60 * 24)

    @property
    def hour(self) -> int:
        """Time.hour -> int"""
        total_hours = self._value // 60
        return total_hours % 24

    @property
    def minute(self) -> int:
        """Time.minute -> int"""
        return self._value % 60

    @property
    def dayname(self) -> str:
        """Time.dayname -> str"""
        return self._weekdays[self.weekday]

    def __lt__(self, other: Time) -> bool:
        """Time < Time -> bool"""
        if isinstance(other, Time):
            return self._value < other._value
        else:
            return NotImplemented

    def __eq__(self, other: Time) -> bool:
        """Time == Time -> bool"""
        if isinstance(other, Time):
            return self._value == other._value
        else:
            return NotImplemented

    def __add__(self, other: int) -> Time:
        """Time + int -> Time"""
        if isinstance(other, int):
            return Time(self._value + other)
        else:
            return NotImplemented

    def __radd__(self, other: int) -> Time:
        """int + Time -> Time"""
        return self.__add__(other)

    def __sub__(self, other: Union[Time, int]) -> Time:
        """
        Time - int -> Time
        Time - Time -> int
        """
        if isinstance(other, Time):
            return self._value - other._value
        elif isinstance(other, int):
            return Time(self._value - other)
        else:
            return NotImplemented
