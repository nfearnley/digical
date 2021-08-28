from __future__ import annotations
from typing import List, Tuple, Union
import bisect

from .timerange import Time, TimeRange


class Schedule:
    def __init__(self, timeranges=()):
        """Schedule() -> Schedule"""
        self._timeranges: List[TimeRange] = []
        for r in timeranges:
            self.add(r)

    @classmethod
    def from_json(cls, j):
        """Schedule.from_json(dict) -> Schedule"""
        timeranges = [TimeRange.from_json(r) for r in j["timeranges"]]
        return cls(timeranges)

    def to_json(self):
        """Schedule.to_json() -> dict"""
        return {
            "timeranges": [TimeRange.to_json(r) for r in self.timeranges]
        }

    def copy(self) -> Schedule:
        """Schedule.copy() -> Schedule"""
        return Schedule(self._timeranges.copy())

    def __repr__(self) -> str:
        """repr(Schedule) -> repr"""
        return f"Schedule({self._timeranges!r})"

    def __str__(self) -> str:
        """str(Schedule) -> str"""
        return "; ".join(str(r) for r in self._timeranges)

    def __len__(self):
        """len(Schedule) -> int"""
        return sum(len(r) for r in self._timeranges)

    @property
    def timeranges(self):
        """Schedule.timeranges -> *TimeRange"""
        return tuple(self._timeranges)

    def __eq__(self, other: Schedule) -> bool:
        """Schedule == Schedule -> bool"""
        if isinstance(other, Schedule):
            return self._timeranges == other._timeranges
        else:
            return NotImplemented

    def __add__(self, other: Union[int, Schedule]) -> Schedule:
        """Schedule + int -> Schedule"""
        if isinstance(other, int):
            timeranges = [r + other for r in self._timeranges]
            return Schedule(timeranges)
        if isinstance(other, Schedule):
            schedule = self.copy()
            schedule += other
            return schedule
        else:
            return NotImplemented

    def __sub__(self, other: Union[int, Schedule]) -> Schedule:
        """Schedule - int -> Schedule"""
        if isinstance(other, int):
            timeranges = [r - other for r in self._timeranges]
            return Schedule(timeranges)
        if isinstance(other, Schedule):
            schedule = self.copy()
            schedule -= other
            return schedule
        else:
            return NotImplemented

    def __radd__(self, other: int) -> int:
        """int + Schedule -> Schedule"""
        if isinstance(other, int):
            return self.__add__(other)
        else:
            return NotImplemented

    def __iadd__(self, other: Union[int, Schedule]) -> Schedule:
        """Schedule += int -> None"""
        if isinstance(other, int):
            self._timeranges = [r + other for r in self._timeranges]
            return self
        if isinstance(other, Schedule):
            for r in other.timeranges:
                self.add(r)
            return self
        else:
            return NotImplemented

    def __isub__(self, other: Union[int, Schedule]) -> Schedule:
        """Schedule - int -> Schedule"""
        if isinstance(other, int):
            self._timeranges = [r - other for r in self._timeranges]
            return self
        if isinstance(other, Schedule):
            self.difference_update(other)
            return self
        else:
            return NotImplemented

    def __contains__(self, other: Time) -> bool:
        """Time in Schedule -> bool"""
        if isinstance(other, Time):
            return any(other in r for r in self._timeranges)
        if isinstance(other, TimeRange):
            return any(other in r for r in self._timeranges)
        else:
            return NotImplemented

    def add(self, timerange: TimeRange) -> None:
        overlapping = []
        for i, r in enumerate(self._timeranges):
            if not timerange_isdisjoint(timerange, r) or timerange_isadjacent(timerange, r):
                overlapping.append(i)

        if not overlapping:
            bisect.insort(self._timeranges, timerange)
        elif len(overlapping) == 1:
            i = overlapping[0]
            timerange = timerange_union(timerange, self._timeranges[i])[0]
            self._timeranges[i] = timerange
        else:
            i = overlapping[0]
            j = overlapping[-1]
            timerange = timerange_union(timerange, self._timeranges[i])[0]
            timerange = timerange_union(timerange, self._timeranges[j])[0]
            self._timeranges[i:j + 1] = (timerange, )

    def remove(self, timerange: TimeRange) -> None:
        if timerange not in self:
            raise KeyError
        self.discard(timerange)

    def discard(self, timerange: TimeRange) -> None:
        overlapping = []
        for i, r in enumerate(self._timeranges):
            if not timerange_isdisjoint(timerange, r):
                overlapping.append(i)

        if not overlapping:
            return
        elif len(overlapping) == 1:
            i = overlapping[0]
            timeranges = timerange_difference(self._timeranges[i], timerange)
            self._timeranges[i:i + 1] = timeranges
        else:
            i = overlapping[0]
            j = overlapping[-1]
            timeranges = timerange_difference(self._timeranges[i], timerange)
            timeranges += timerange_difference(self._timeranges[j], timerange)
            self._timeranges[i:j + 1] = timeranges

    def pop(self) -> TimeRange:
        try:
            return self._timeranges.pop()
        except IndexError:
            raise KeyError

    def isdisjoint(self, other: Schedule) -> bool:
        ranges_a = iter(self._timeranges)
        ranges_b = iter(other._timeranges)
        try:
            timerange_a = next(ranges_a)
            timerange_b = next(ranges_b)
            while True:
                if not timerange_isdisjoint(timerange_a, timerange_b):
                    return False
                if timerange_a < timerange_b:
                    timerange_a = next(ranges_a)
                else:
                    timerange_b = next(ranges_b)
        except StopIteration:
            return True

    def issubset(self, other: Schedule) -> bool:
        if not other._timeranges:
            return True
        ranges_a = iter(self._timeranges)
        try:
            timerange_a = next(ranges_a)
            for timerange_b in other._timeranges:
                if timerange_b.start < timerange_a.start:
                    return False
                if timerange_issubset(timerange_a, timerange_b):
                    continue
                timerange_a = next(ranges_a)
        except StopIteration:
            return False
        return True

    def __le__(self, other: Schedule) -> bool:
        return other.issubset(self)

    def __lt__(self, other: Schedule) -> bool:
        if self == other:
            return False
        return other.issubset(self)

    def issuperset(self, other: Schedule) -> bool:
        return other.issubset(self)

    def __ge__(self, other: Schedule) -> bool:
        return other.issuperset(self)

    def __gt__(self, other: Schedule) -> bool:
        if self == other:
            return False
        return other.issuperset(self)

    def union(self, *others: Schedule) -> Schedule:
        schedule = self.copy()
        schedule.update(*others)
        return schedule

    def __or__(self, other: Schedule) -> Schedule:
        return self.union(other)

    def intersection(self, *others: Schedule) -> Schedule:
        schedule = self.copy()
        schedule.intersection_update(*others)
        return schedule

    def __and__(self, other: Schedule) -> Schedule:
        return self.intersection(other)

    def difference(self, *others: Schedule) -> Schedule:
        schedule = self.copy()
        schedule.difference_update(*others)
        return schedule

    def sub(self, other: Schedule) -> Schedule:
        return self.difference(other)

    def symmetric_difference(self, other: Schedule) -> Schedule:
        unioned = self.union(other)
        intersectioned = self.intersection(other)
        schedule = unioned - intersectioned
        return schedule

    def __xor__(self, other: Schedule) -> Schedule:
        return self.symmetric_difference(other)

    def update(self, *others: Schedule) -> None:
        for other in others:
            for r in other._timeranges:
                self.add(r)

    def __ior__(self, other: Schedule) -> None:
        self.update(other)
        return self

    def intersection_update(self, *others: Schedule) -> None:
        if any(not o._timeranges for o in others):
            self._timeranges.clear()
            return

        for other in others:
            new_ranges = []
            other_iter = iter(other._timeranges)
            other_r = next(other_iter)
            for r in self._timeranges:
                for other_r in other.timeranges:
                    new_ranges.extend(timerange_intersection(r, other_r))
            self._timeranges = new_ranges
            if not self._timeranges:
                return

    def __iand__(self, other: Schedule) -> None:
        self.intersection_update(other)
        return self

    def difference_update(self, *others: Schedule) -> None:
        for other in others:
            for r in other._timeranges:
                self.discard(r)

    def symmetric_difference_update(self, other: Schedule) -> Schedule:
        schedule = self.symmetric_difference(other)
        self._timeranges = schedule._timeranges
        return self

    def __ixor__(self, other: Schedule) -> Schedule:
        return self.symmetric_difference_update(other)


def timerange_isdisjoint(timerange_a: TimeRange, timerange_b: TimeRange) -> bool:
    return (
        timerange_a.end <= timerange_b.start
        or timerange_b.end <= timerange_a.start
    )


def timerange_isadjacent(timerange_a: TimeRange, timerange_b: TimeRange) -> bool:
    return (
        timerange_a.start == timerange_b.end
        or timerange_b.start == timerange_a.end
    )


def timerange_issubset(timerange_a: TimeRange, timerange_b: TimeRange) -> bool:
    return (
        timerange_b.start >= timerange_a.start
        and timerange_b.end <= timerange_a.end
    )


def timerange_ispropersubset(timerange_a: TimeRange, timerange_b: TimeRange) -> bool:
    return (
        timerange_b.start >= timerange_a.start
        and timerange_b.end <= timerange_a.end
        and timerange_a != timerange_b
    )


def timerange_issuperset(timerange_a: TimeRange, timerange_b: TimeRange) -> bool:
    return (
        timerange_a.start >= timerange_b.start
        and timerange_a.end <= timerange_b.end
    )


def timerange_ispropersuperset(timerange_a: TimeRange, timerange_b: TimeRange) -> bool:
    return (
        timerange_a.start >= timerange_b.start
        and timerange_a.end <= timerange_b.end
        and timerange_a != timerange_b
    )


def timerange_union(timerange_a: TimeRange, timerange_b: TimeRange) -> Tuple[TimeRange, ...]:
    if timerange_isdisjoint(timerange_a, timerange_b) and not timerange_isadjacent(timerange_a, timerange_b):
        return tuple(sorted((timerange_a, timerange_b)))
    else:
        return (TimeRange(min(timerange_a.start, timerange_b.start), max(timerange_a.end, timerange_b.end)), )


def timerange_intersection(timerange_a: TimeRange, timerange_b: TimeRange) -> Tuple[TimeRange, ...]:
    if timerange_isdisjoint(timerange_a, timerange_b):
        return ()
    else:
        return (TimeRange(max(timerange_a.start, timerange_b.start), min(timerange_a.end, timerange_b.end)), )


def timerange_difference(timerange_a: TimeRange, timerange_b: TimeRange) -> Tuple[TimeRange, ...]:
    if timerange_isdisjoint(timerange_a, timerange_b):
        return (timerange_a, )
    elif timerange_a.start < timerange_b.start < timerange_a.end and timerange_a.start < timerange_b.end < timerange_a.end:
        return (TimeRange(timerange_a.start, timerange_b.start), TimeRange(timerange_b.end, timerange_a.end))
    elif timerange_a.start < timerange_b.start < timerange_a.end:
        return (TimeRange(timerange_a.start, timerange_b.start), )
    elif timerange_a.start < timerange_b.end < timerange_a.end:
        return (TimeRange(timerange_b.end, timerange_a.end), )
    else:
        return ()


def timerange_symmetric_difference(timerange_a: TimeRange, timerange_b: TimeRange) -> Tuple[TimeRange, ...]:
    if timerange_isdisjoint(timerange_a, timerange_b):
        return timerange_union(timerange_a, timerange_b)
    elif timerange_a == timerange_b:
        return ()
    else:
        return timerange_difference(timerange_union(timerange_a, timerange_b)[0], timerange_intersection(timerange_a, timerange_b)[0])
