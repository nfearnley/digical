import pytest

from digical import Time, TimeRange, Schedule
from digical.lib.schedule import timerange_isdisjoint, timerange_isadjacent, timerange_issubset, timerange_ispropersubset, timerange_issuperset, timerange_ispropersuperset, timerange_union, timerange_intersection, timerange_difference, timerange_symmetric_difference


def test_init():
    """Schedule() -> Schedule"""
    schedule_empty = Schedule()
    assert schedule_empty is not None
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    assert schedule is not None


def test_from_json():
    """Schedule.from_json(dict) -> Schedule"""
    schedule = Schedule.from_json({
        "timeranges": [
            {
                "start": {"value": 1000},
                "end": {"value": 2000}
            },
            {
                "start": {"value": 2500},
                "end": {"value": 3000}
            }
        ]
    })
    assert schedule == Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])


def test_to_json():
    """Schedule.to_json() -> dict"""
    schedule_json = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ]).to_json()
    assert schedule_json == {
        "timeranges": [
            {
                "start": {"value": 1000},
                "end": {"value": 2000}
            },
            {
                "start": {"value": 2500},
                "end": {"value": 3000}
            }
        ]
    }


def test_copy():
    """Schedule.copy() -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = schedule_a.copy()
    assert schedule_a == schedule_b
    assert schedule_a is not schedule_b


def test_repr():
    """repr(Schedule) -> repr"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    assert repr(schedule) == "Schedule([TimeRange(Time(1000), Time(2000)), TimeRange(Time(2500), Time(3000))])"


def test_str():
    """str(Schedule) -> str"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    assert str(schedule) == "Sunday, 16:40 - Monday, 9:20; Monday, 17:40 - Tuesday, 2:00"


def test_len():
    """len(Schedule) -> int"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    assert len(schedule) == 1500


def test_timeranges():
    """Schedule.timeranges -> *TimeRange"""
    timeranges = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ]).timeranges
    assert isinstance(timeranges, tuple)
    assert timeranges == (
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    )


def test_eq():
    """Schedule == Schedule -> bool"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1500), Time(2500))
    ])
    assert schedule_a == schedule_b
    assert not schedule_a == schedule_c


def test_add_int():
    """Schedule + int -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = schedule_a + 500
    assert schedule_b == Schedule([
        TimeRange(Time(1500), Time(2500)),
        TimeRange(Time(3000), Time(3500))
    ])


def test_sub_int():
    """Schedule - int -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = schedule_a - 500
    assert schedule_b == Schedule([
        TimeRange(Time(500), Time(1500)),
        TimeRange(Time(2000), Time(2500))
    ])


def test_radd_int():
    """int + Schedule -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = 500 + schedule_a
    assert schedule_b == Schedule([
        TimeRange(Time(1500), Time(2500)),
        TimeRange(Time(3000), Time(3500))
    ])


def test_iadd_int():
    """Schedule += int -> None"""
    schedule_orig = schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule += 500
    assert schedule == Schedule([
        TimeRange(Time(1500), Time(2500)),
        TimeRange(Time(3000), Time(3500))
    ])
    assert schedule is schedule_orig


def test_isub_int():
    """Schedule -= int -> None"""
    schedule_orig = schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule -= 500
    assert schedule == Schedule([
        TimeRange(Time(500), Time(1500)),
        TimeRange(Time(2000), Time(2500))
    ])
    assert schedule is schedule_orig


def test_contains_time():
    """Time in Schedule -> bool"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    assert (Time(500) in schedule) is False
    assert (Time(1000) in schedule) is True
    assert (Time(1500) in schedule) is True
    assert (Time(2000) in schedule) is False
    assert (Time(2250) in schedule) is False
    assert (Time(2500) in schedule) is True
    assert (Time(2750) in schedule) is True
    assert (Time(3000) in schedule) is False
    assert (Time(3500) in schedule) is False


def test_contains_timerange():
    """TimeRange in Schedule -> bool"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    assert (TimeRange(Time(500), Time(750)) in schedule) is False
    assert (TimeRange(Time(500), Time(1500)) in schedule) is False
    assert (TimeRange(Time(1000), Time(2000)) in schedule) is True
    assert (TimeRange(Time(1200), Time(1800)) in schedule) is True
    assert (TimeRange(Time(1200), Time(2800)) in schedule) is False


def test_add_timerange():
    """Schedule.add(TimeRange) -> None"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule.add(TimeRange(Time(2000), Time(2500)))
    assert schedule == Schedule([
        TimeRange(Time(1000), Time(3000))
    ])

    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule.add(TimeRange(Time(1200), Time(2700)))
    assert schedule == Schedule([
        TimeRange(Time(1000), Time(3000))
    ])

    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule.add(TimeRange(Time(2200), Time(2700)))
    assert schedule == Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2200), Time(3000))
    ])


def test_remove_timerange():
    """Schedule.remove(TimeRange) -> None"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule.remove(TimeRange(Time(1000), Time(1200)))
    assert schedule == Schedule([
        TimeRange(Time(1200), Time(2000))
    ])

    schedule = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    with pytest.raises(KeyError):
        schedule.remove(TimeRange(Time(800), Time(1200)))


def test_discard_timerange():
    """Schedule.discard(TimeRange) -> None"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule.discard(TimeRange(Time(1000), Time(1200)))
    assert schedule == Schedule([
        TimeRange(Time(1200), Time(2000))
    ])

    schedule = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule.discard(TimeRange(Time(800), Time(1200)))
    assert schedule == Schedule([
        TimeRange(Time(1200), Time(2000))
    ])


def test_pop():
    """Schedule.pop() -> elem"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    timerange = schedule.pop()
    assert schedule == Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    assert timerange == TimeRange(Time(2500), Time(3000))


def test_add_schedule():
    """Schedule + Schedule -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1500), Time(2500))
    ])
    assert schedule_a + schedule_b == Schedule([
        TimeRange(Time(1000), Time(2500))
    ])


def test_sub_schedule():
    """Schedule - Schedule -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1500), Time(2500))
    ])
    assert schedule_a - schedule_b == Schedule([
        TimeRange(Time(1000), Time(1500))
    ])


def test_iadd_schedule():
    """Schedule += Schedule -> None"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule += Schedule([
        TimeRange(Time(1500), Time(2500))
    ])
    assert schedule == Schedule([
        TimeRange(Time(1000), Time(2500))
    ])


def test_isub_schedule():
    """Schedule -= Schedule -> None"""
    schedule = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule -= Schedule([
        TimeRange(Time(1500), Time(2500))
    ])
    assert schedule == Schedule([
        TimeRange(Time(1000), Time(1500))
    ])


def test_isdisjoint():
    """Schedule.isdisjoint(Schedule) -> bool"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1500), Time(2500))
    ])
    schedule_c = Schedule([
        TimeRange(Time(2000), Time(3000))
    ])
    assert schedule_a.isdisjoint(schedule_b) is False
    assert schedule_a.isdisjoint(schedule_c) is True


def test_issubset():
    """Schedule.issubset(Schedule) -> bool"""
    """Schedule <= Schedule -> bool"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1500), Time(2000))
    ])
    schedule_d = Schedule([
        TimeRange(Time(1500), Time(3000))
    ])
    assert schedule_a.issubset(schedule_b) is True
    assert schedule_a.issubset(schedule_c) is True
    assert schedule_a.issubset(schedule_d) is False
    assert (schedule_b <= schedule_a) is True
    assert (schedule_c <= schedule_a) is True
    assert (schedule_d <= schedule_a) is False


def test_ispropersubset():
    """Schedule < Schedule -> bool"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1500), Time(2000))
    ])
    schedule_d = Schedule([
        TimeRange(Time(1500), Time(3000))
    ])
    assert not schedule_b < schedule_a
    assert schedule_c < schedule_a
    assert not schedule_d < schedule_a


def test_issuperset():
    """Schedule.issuperset(Schedule) -> bool"""
    """Schedule >= Schedule -> bool"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_c = Schedule([
        TimeRange(Time(500), Time(2000))
    ])
    schedule_d = Schedule([
        TimeRange(Time(500), Time(1500))
    ])
    assert schedule_a.issuperset(schedule_b)
    assert schedule_a.issuperset(schedule_c)
    assert not schedule_a.issuperset(schedule_d)
    assert schedule_b >= schedule_a
    assert schedule_c >= schedule_a
    assert not schedule_d >= schedule_a


def test_ispropersuperset():
    """Schedule > Schedule -> bool"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1000), Time(2000))
    ])
    schedule_c = Schedule([
        TimeRange(Time(500), Time(2000))
    ])
    schedule_d = Schedule([
        TimeRange(Time(500), Time(1500))
    ])
    assert not schedule_b > schedule_a
    assert schedule_c > schedule_a
    assert not schedule_d > schedule_a


def test_union():
    """Schedule.union(*Schedule) -> Schedule"""
    """Schedule | Schedule -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(4500), Time(6000))
    ])
    assert schedule_a.union(schedule_b, schedule_c) == Schedule([
        TimeRange(Time(1000), Time(2200)),
        TimeRange(Time(2500), Time(3200)),
        TimeRange(Time(4500), Time(6000))
    ])
    assert schedule_a | schedule_b == Schedule([
        TimeRange(Time(1000), Time(2200)),
        TimeRange(Time(2500), Time(3200))
    ])


def test_intersection():
    """Schedule.intersection(*Schedule) -> Schedule"""
    """Schedule & Schedule -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1300), Time(6000))
    ])
    assert schedule_a.intersection(schedule_b, schedule_c) == Schedule([
        TimeRange(Time(1300), Time(2000)),
        TimeRange(Time(2700), Time(3000))
    ])
    assert schedule_a & schedule_b == Schedule([
        TimeRange(Time(1200), Time(2000)),
        TimeRange(Time(2700), Time(3000))
    ])


def test_difference():
    """Schedule.difference(*Schedule) -> Schedule"""
    """Schedule - Schedule -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1300), Time(6000))
    ])
    assert schedule_a.difference(schedule_b, schedule_c) == Schedule([
        TimeRange(Time(1000), Time(1200))
    ])
    assert schedule_a - schedule_b == Schedule([
        TimeRange(Time(1000), Time(1200)),
        TimeRange(Time(2500), Time(2700))
    ])


def test_symmetric_difference():
    """Schedule.symmetric_difference(Schedule) -> Schedule"""
    """Schedule ^ Schedule -> Schedule"""
    schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    assert schedule_a.symmetric_difference(schedule_b) == Schedule([
        TimeRange(Time(1000), Time(1200)),
        TimeRange(Time(2000), Time(2200)),
        TimeRange(Time(2500), Time(2700)),
        TimeRange(Time(3000), Time(3200))
    ])
    assert schedule_a ^ schedule_b == Schedule([
        TimeRange(Time(1000), Time(1200)),
        TimeRange(Time(2000), Time(2200)),
        TimeRange(Time(2500), Time(2700)),
        TimeRange(Time(3000), Time(3200))
    ])


def test_update():
    """Schedule.update(*Schedule) -> None"""
    """Schedule |= Schedule -> None"""
    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(4500), Time(6000))
    ])
    schedule_a.update(schedule_b, schedule_c)
    assert schedule_a == Schedule([
        TimeRange(Time(1000), Time(2200)),
        TimeRange(Time(2500), Time(3200)),
        TimeRange(Time(4500), Time(6000))
    ])
    assert schedule_a is schedule_orig

    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(4500), Time(6000))
    ])
    schedule_a |= schedule_b
    assert schedule_a == Schedule([
        TimeRange(Time(1000), Time(2200)),
        TimeRange(Time(2500), Time(3200))
    ])
    assert schedule_a is schedule_orig


def test_intersection_update():
    """Schedule.intersection_update(*Schedule) -> None"""
    """Schedule &= Schedule -> None"""
    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1300), Time(6000))
    ])
    schedule_a.intersection_update(schedule_b, schedule_c)
    assert schedule_a == Schedule([
        TimeRange(Time(1300), Time(2000)),
        TimeRange(Time(2700), Time(3000))
    ])
    assert schedule_a is schedule_orig

    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1300), Time(6000))
    ])
    schedule_a &= schedule_b
    assert schedule_a == Schedule([
        TimeRange(Time(1200), Time(2000)),
        TimeRange(Time(2700), Time(3000))
    ])
    assert schedule_a is schedule_orig


def test_difference_update():
    """Schedule.difference_update(*Schedule) -> None"""
    """Schedule -= Schedule -> None"""
    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1300), Time(6000))
    ])
    schedule_a.difference_update(schedule_b, schedule_c)
    assert schedule_a == Schedule([
        TimeRange(Time(1000), Time(1200))
    ])
    assert schedule_a is schedule_orig

    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_c = Schedule([
        TimeRange(Time(1300), Time(6000))
    ])
    schedule_a -= schedule_b
    assert schedule_a - schedule_b == Schedule([
        TimeRange(Time(1000), Time(1200)),
        TimeRange(Time(2500), Time(2700))
    ])
    assert schedule_a is schedule_orig


def test_symmetric_difference_update():
    """Schedule.symmetric_difference_update(Schedule) -> None"""
    """Schedule ^= Schedule -> None"""
    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_a.symmetric_difference_update(schedule_b)
    assert schedule_a == Schedule([
        TimeRange(Time(1000), Time(1200)),
        TimeRange(Time(2000), Time(2200)),
        TimeRange(Time(2500), Time(2700)),
        TimeRange(Time(3000), Time(3200))
    ])
    assert schedule_a is schedule_orig

    schedule_orig = schedule_a = Schedule([
        TimeRange(Time(1000), Time(2000)),
        TimeRange(Time(2500), Time(3000))
    ])
    schedule_b = Schedule([
        TimeRange(Time(1200), Time(2200)),
        TimeRange(Time(2700), Time(3200))
    ])
    schedule_a ^= schedule_b
    assert schedule_a == Schedule([
        TimeRange(Time(1000), Time(1200)),
        TimeRange(Time(2000), Time(2200)),
        TimeRange(Time(2500), Time(2700)),
        TimeRange(Time(3000), Time(3200))
    ])
    assert schedule_a is schedule_orig


def test_timerange_isdisjoint():
    """timerange_isdisjoint(TimeRange, TimeRange) -> bool"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_isdisjoint(timerange_a, timerange_b) is True
    assert timerange_isdisjoint(timerange_a, timerange_c) is True
    assert timerange_isdisjoint(timerange_a, timerange_d) is False
    assert timerange_isdisjoint(timerange_a, timerange_e) is False
    assert timerange_isdisjoint(timerange_a, timerange_f) is False
    assert timerange_isdisjoint(timerange_a, timerange_g) is True
    assert timerange_isdisjoint(timerange_a, timerange_h) is True
    assert timerange_isdisjoint(timerange_a, timerange_i) is False
    assert timerange_isdisjoint(timerange_a, timerange_j) is False
    assert timerange_isdisjoint(timerange_a, timerange_k) is False
    assert timerange_isdisjoint(timerange_a, timerange_l) is False
    assert timerange_isdisjoint(timerange_a, timerange_m) is False
    assert timerange_isdisjoint(timerange_a, timerange_n) is False


def test_timerange_isadjacent():
    """timerange_isadjacent(TimeRange, TimeRange) -> bool"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_isadjacent(timerange_a, timerange_b) is False
    assert timerange_isadjacent(timerange_a, timerange_c) is True
    assert timerange_isadjacent(timerange_a, timerange_d) is False
    assert timerange_isadjacent(timerange_a, timerange_e) is False
    assert timerange_isadjacent(timerange_a, timerange_f) is False
    assert timerange_isadjacent(timerange_a, timerange_g) is True
    assert timerange_isadjacent(timerange_a, timerange_h) is False
    assert timerange_isadjacent(timerange_a, timerange_i) is False
    assert timerange_isadjacent(timerange_a, timerange_j) is False
    assert timerange_isadjacent(timerange_a, timerange_k) is False
    assert timerange_isadjacent(timerange_a, timerange_l) is False
    assert timerange_isadjacent(timerange_a, timerange_m) is False
    assert timerange_isadjacent(timerange_a, timerange_n) is False


def test_timerange_issubset():
    """timerange_issubset(TimeRange, TimeRange) -> bool"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_issubset(timerange_a, timerange_b) is False
    assert timerange_issubset(timerange_a, timerange_c) is False
    assert timerange_issubset(timerange_a, timerange_d) is False
    assert timerange_issubset(timerange_a, timerange_e) is True
    assert timerange_issubset(timerange_a, timerange_f) is False
    assert timerange_issubset(timerange_a, timerange_g) is False
    assert timerange_issubset(timerange_a, timerange_h) is False
    assert timerange_issubset(timerange_a, timerange_i) is True
    assert timerange_issubset(timerange_a, timerange_j) is True
    assert timerange_issubset(timerange_a, timerange_k) is True
    assert timerange_issubset(timerange_a, timerange_l) is False
    assert timerange_issubset(timerange_a, timerange_m) is False
    assert timerange_issubset(timerange_a, timerange_n) is False


def test_timerange_ispropersubset():
    """timerange_ispropersubset(TimeRange, TimeRange) -> bool"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_ispropersubset(timerange_a, timerange_b) is False
    assert timerange_ispropersubset(timerange_a, timerange_c) is False
    assert timerange_ispropersubset(timerange_a, timerange_d) is False
    assert timerange_ispropersubset(timerange_a, timerange_e) is False
    assert timerange_ispropersubset(timerange_a, timerange_f) is False
    assert timerange_ispropersubset(timerange_a, timerange_g) is False
    assert timerange_ispropersubset(timerange_a, timerange_h) is False
    assert timerange_ispropersubset(timerange_a, timerange_i) is True
    assert timerange_ispropersubset(timerange_a, timerange_j) is True
    assert timerange_ispropersubset(timerange_a, timerange_k) is True
    assert timerange_ispropersubset(timerange_a, timerange_l) is False
    assert timerange_ispropersubset(timerange_a, timerange_m) is False
    assert timerange_ispropersubset(timerange_a, timerange_n) is False


def test_timerange_issuperset():
    """timerange_issuperset(TimeRange, TimeRange) -> bool"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_issuperset(timerange_a, timerange_b) is False
    assert timerange_issuperset(timerange_a, timerange_c) is False
    assert timerange_issuperset(timerange_a, timerange_d) is False
    assert timerange_issuperset(timerange_a, timerange_e) is True
    assert timerange_issuperset(timerange_a, timerange_f) is False
    assert timerange_issuperset(timerange_a, timerange_g) is False
    assert timerange_issuperset(timerange_a, timerange_h) is False
    assert timerange_issuperset(timerange_a, timerange_i) is False
    assert timerange_issuperset(timerange_a, timerange_j) is False
    assert timerange_issuperset(timerange_a, timerange_k) is False
    assert timerange_issuperset(timerange_a, timerange_l) is True
    assert timerange_issuperset(timerange_a, timerange_m) is True
    assert timerange_issuperset(timerange_a, timerange_n) is True


def test_timerange_ispropersuperset():
    """timerange_ispropersuperset(TimeRange, TimeRange) -> bool"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_ispropersuperset(timerange_a, timerange_b) is False
    assert timerange_ispropersuperset(timerange_a, timerange_c) is False
    assert timerange_ispropersuperset(timerange_a, timerange_d) is False
    assert timerange_ispropersuperset(timerange_a, timerange_e) is False
    assert timerange_ispropersuperset(timerange_a, timerange_f) is False
    assert timerange_ispropersuperset(timerange_a, timerange_g) is False
    assert timerange_ispropersuperset(timerange_a, timerange_h) is False
    assert timerange_ispropersuperset(timerange_a, timerange_i) is False
    assert timerange_ispropersuperset(timerange_a, timerange_j) is False
    assert timerange_ispropersuperset(timerange_a, timerange_k) is False
    assert timerange_ispropersuperset(timerange_a, timerange_l) is True
    assert timerange_ispropersuperset(timerange_a, timerange_m) is True
    assert timerange_ispropersuperset(timerange_a, timerange_n) is True


def test_timerange_union():
    """timerange_union(TimeRange, TimeRange) -> TimeRange"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_union(timerange_a, timerange_b) == (TimeRange(Time(1000), Time(2000)), TimeRange(Time(2500), Time(3000)))
    assert timerange_union(timerange_a, timerange_c) == (TimeRange(Time(1000), Time(2500)), )
    assert timerange_union(timerange_a, timerange_d) == (TimeRange(Time(1000), Time(2500)), )
    assert timerange_union(timerange_a, timerange_e) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_union(timerange_a, timerange_f) == (TimeRange(Time(500), Time(2000)), )
    assert timerange_union(timerange_a, timerange_g) == (TimeRange(Time(500), Time(2000)), )
    assert timerange_union(timerange_a, timerange_h) == (TimeRange(Time(0), Time(500)), TimeRange(Time(1000), Time(2000)))
    assert timerange_union(timerange_a, timerange_i) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_union(timerange_a, timerange_j) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_union(timerange_a, timerange_k) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_union(timerange_a, timerange_l) == (TimeRange(Time(1000), Time(2500)), )
    assert timerange_union(timerange_a, timerange_m) == (TimeRange(Time(500), Time(2500)), )
    assert timerange_union(timerange_a, timerange_n) == (TimeRange(Time(500), Time(2000)), )


def test_timerange_intersection():
    """timerange_intersection(TimeRange, TimeRange) -> TimeRange"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_intersection(timerange_a, timerange_b) == ()
    assert timerange_intersection(timerange_a, timerange_c) == ()
    assert timerange_intersection(timerange_a, timerange_d) == (TimeRange(Time(1500), Time(2000)), )
    assert timerange_intersection(timerange_a, timerange_e) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_intersection(timerange_a, timerange_f) == (TimeRange(Time(1000), Time(1500)), )
    assert timerange_intersection(timerange_a, timerange_g) == ()
    assert timerange_intersection(timerange_a, timerange_h) == ()
    assert timerange_intersection(timerange_a, timerange_i) == (TimeRange(Time(1500), Time(2000)), )
    assert timerange_intersection(timerange_a, timerange_j) == (TimeRange(Time(1200), Time(1800)), )
    assert timerange_intersection(timerange_a, timerange_k) == (TimeRange(Time(1000), Time(1500)), )
    assert timerange_intersection(timerange_a, timerange_l) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_intersection(timerange_a, timerange_m) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_intersection(timerange_a, timerange_n) == (TimeRange(Time(1000), Time(2000)), )


def test_timerange_difference():
    """timerange_difference(TimeRange, TimeRange) -> TimeRange"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_difference(timerange_a, timerange_b) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_difference(timerange_a, timerange_c) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_difference(timerange_a, timerange_d) == (TimeRange(Time(1000), Time(1500)), )
    assert timerange_difference(timerange_a, timerange_e) == ()
    assert timerange_difference(timerange_a, timerange_f) == (TimeRange(Time(1500), Time(2000)), )
    assert timerange_difference(timerange_a, timerange_g) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_difference(timerange_a, timerange_h) == (TimeRange(Time(1000), Time(2000)), )
    assert timerange_difference(timerange_a, timerange_i) == (TimeRange(Time(1000), Time(1500)), )
    assert timerange_difference(timerange_a, timerange_j) == (TimeRange(Time(1000), Time(1200)), TimeRange(Time(1800), Time(2000)))
    assert timerange_difference(timerange_a, timerange_k) == (TimeRange(Time(1500), Time(2000)), )
    assert timerange_difference(timerange_a, timerange_l) == ()
    assert timerange_difference(timerange_a, timerange_m) == ()
    assert timerange_difference(timerange_a, timerange_n) == ()


def test_timerange_symmetric_difference():
    """timerange_symmetric_difference(TimeRange, TimeRange) -> TimeRange"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = TimeRange(Time(2500), Time(3000))
    timerange_c = TimeRange(Time(2000), Time(2500))
    timerange_d = TimeRange(Time(1500), Time(2500))
    timerange_e = TimeRange(Time(1000), Time(2000))
    timerange_f = TimeRange(Time(500), Time(1500))
    timerange_g = TimeRange(Time(500), Time(1000))
    timerange_h = TimeRange(Time(0), Time(500))
    timerange_i = TimeRange(Time(1500), Time(2000))
    timerange_j = TimeRange(Time(1200), Time(1800))
    timerange_k = TimeRange(Time(1000), Time(1500))
    timerange_l = TimeRange(Time(1000), Time(2500))
    timerange_m = TimeRange(Time(500), Time(2500))
    timerange_n = TimeRange(Time(500), Time(2000))
    assert timerange_symmetric_difference(timerange_a, timerange_b) == (TimeRange(Time(1000), Time(2000)), TimeRange(Time(2500), Time(3000)))
    assert timerange_symmetric_difference(timerange_a, timerange_c) == (TimeRange(Time(1000), Time(2500)), )
    assert timerange_symmetric_difference(timerange_a, timerange_d) == (TimeRange(Time(1000), Time(1500)), TimeRange(Time(2000), Time(2500)))
    assert timerange_symmetric_difference(timerange_a, timerange_e) == ()
    assert timerange_symmetric_difference(timerange_a, timerange_f) == (TimeRange(Time(500), Time(1000)), TimeRange(Time(1500), Time(2000)))
    assert timerange_symmetric_difference(timerange_a, timerange_g) == (TimeRange(Time(500), Time(2000)), )
    assert timerange_symmetric_difference(timerange_a, timerange_h) == (TimeRange(Time(0), Time(500)), TimeRange(Time(1000), Time(2000)))
    assert timerange_symmetric_difference(timerange_a, timerange_i) == (TimeRange(Time(1000), Time(1500)), )
    assert timerange_symmetric_difference(timerange_a, timerange_j) == (TimeRange(Time(1000), Time(1200)), TimeRange(Time(1800), Time(2000)))
    assert timerange_symmetric_difference(timerange_a, timerange_k) == (TimeRange(Time(1500), Time(2000)), )
    assert timerange_symmetric_difference(timerange_a, timerange_l) == (TimeRange(Time(2000), Time(2500)), )
    assert timerange_symmetric_difference(timerange_a, timerange_m) == (TimeRange(Time(500), Time(1000)), TimeRange(Time(2000), Time(2500)))
    assert timerange_symmetric_difference(timerange_a, timerange_n) == (TimeRange(Time(500), Time(1000)), )
