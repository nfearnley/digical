from __future__ import annotations
from typing import Union

from .time import Time


class TimeRange:
    def __init__(self, start: Time, end: Time):
        """TimeRange(Time, Time) -> TimeRange"""
        if start >= end:
            raise ValueError("Invalid TimeRange: start must be less than end")
        self._start = start
        self._end = end

    @classmethod
    def from_json(cls, j: dict) -> TimeRange:
        """TimeRange.from_json(dict) -> TimeRange"""
        return TimeRange(
            Time.from_json(j["start"]),
            Time.from_json(j["end"])
        )

    def to_json(self) -> dict:
        """TimeRange.to_json() -> dict"""
        return {
            "start": self.start.to_json(),
            "end": self.end.to_json()
        }

    def copy(self) -> TimeRange:
        """TimeRange.copy() -> TimeRange"""
        return TimeRange(
            self.start.copy(),
            self.end.copy()
        )

    def __hash__(self) -> int:
        """hash(TimeRange) -> int"""
        return hash((self.start, self.end))

    def __repr__(self) -> str:
        return f"TimeRange({self.start!r}, {self.end!r})"

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"

    def __len__(self) -> int:
        """len(TimeRange) -> int"""
        return self.end - self.start

    @property
    def start(self) -> int:
        """Time.start -> int"""
        return self._start

    @property
    def end(self) -> int:
        """Time.end -> int"""
        return self._end

    def __add__(self, other: int) -> int:
        """TimeRange + int -> TimeRange"""
        if isinstance(other, int):
            start = self.start + other
            end = self.end + other
            return TimeRange(start, end)
        else:
            return NotImplemented

    def __sub__(self, other: int) -> int:
        """TimeRange - int -> TimeRange"""
        if isinstance(other, int):
            return self.__add__(-other)
        else:
            return NotImplemented

    def __radd__(self, other: int) -> int:
        """int + TimeRange -> TimeRange"""
        if isinstance(other, int):
            return self.__add__(other)
        else:
            return NotImplemented

    def __contains__(self, other: Union[Time, TimeRange]):
        """Time in TimeRange -> bool"""
        """TimeRange in TimeRange -> bool"""
        if isinstance(other, Time):
            return other >= self.start and other < self.end
        elif isinstance(other, TimeRange):
            return other.start >= self.start and other.end <= self.end
        else:
            return NotImplemented

    def __lt__(self, other: Time):
        """Time < TimeRange -> bool"""
        """TimeRange < TimeRange -> bool"""
        if isinstance(other, Time):
            return self.end <= other
        elif isinstance(other, TimeRange):
            return (self.start, self.end) < (other.start, other.end)
        else:
            return NotImplemented

    def __le__(self, other: Time):
        """Time <= TimeRange -> bool"""
        """TimeRange <= TimeRange -> bool"""
        if isinstance(other, Time):
            return self.start <= other
        elif isinstance(other, TimeRange):
            return (self.start, self.end) <= (other.start, other.end)
        else:
            return NotImplemented

    def __eq__(self, other: Time):
        """TimeRange == TimeRange -> bool"""
        if isinstance(other, TimeRange):
            return (self.start, self.end) == (other.start, other.end)
        else:
            return NotImplemented

    def __ne__(self, other: Time):
        """TimeRange != TimeRange -> bool"""
        return not self.__eq__(other)

    def __gt__(self, other: Time):
        """Time > TimeRange -> bool"""
        """TimeRange > TimeRange -> bool"""
        if isinstance(other, Time):
            return self.start > other
        elif isinstance(other, TimeRange):
            return (self.start, self.end) > (other.start, other.end)
        else:
            return NotImplemented

    def __ge__(self, other: Time):
        """Time >= TimeRange -> bool"""
        """TimeRange >= TimeRange -> bool"""
        if isinstance(other, Time):
            return self.end > other
        elif isinstance(other, TimeRange):
            return (self.start, self.end) >= (other.start, other.end)
        else:
            return NotImplemented
