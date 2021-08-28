import pytest
from digical import Time, TimeRange


def test_init():
    """TimeRange(Time, Time) -> TimeRange"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert timerange is not None
    with pytest.raises(ValueError):
        TimeRange(Time(1000), Time(1000))
    with pytest.raises(ValueError):
        TimeRange(Time(2000), Time(1000))


def test_from_json():
    """TimeRange.from_json(dict) -> TimeRange"""
    timerange = TimeRange.from_json({
        "start": {"value": 1000},
        "end": {"value": 2000}
    })
    assert timerange.start == Time(1000) and timerange.end == Time(2000)


def test_to_json():
    """TimeRange.to_json() -> dict"""
    timerange_json = TimeRange(Time(1000), Time(2000)).to_json()
    assert timerange_json["start"]["value"] == 1000 and timerange_json["end"]["value"] == 2000


def test_copy():
    """TimeRange.copy() -> TimeRange"""
    timerange_a = TimeRange(Time(1000), Time(2000))
    timerange_b = timerange_a.copy()
    assert timerange_a == timerange_b
    assert timerange_a is not timerange_b


def test_hash():
    """hash(TimeRange) -> int"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert isinstance(hash(timerange), int)


def test_repr():
    """repr(TimeRange) -> str"""
    timerange = TimeRange(Time(1563), Time(3126))
    assert repr(timerange) == "TimeRange(Time(1563), Time(3126))"


def test_str():
    """str(TimeRange) -> str"""
    timerange = TimeRange(Time(1563), Time(3126))
    assert str(timerange) == "Monday, 2:03 - Tuesday, 4:06"


def test_len():
    """len(TimeRange) -> int"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert len(timerange) == 1000


def test_add_int():
    """TimeRange + int -> TimeRange"""
    timerange = TimeRange(Time(1000), Time(2000)) + 500
    assert timerange.start == Time(1500) and timerange.end == Time(2500)


def test_sub_int():
    """TimeRange - int -> TimeRange"""
    timerange = TimeRange(Time(1000), Time(2000)) - 500
    assert timerange.start == Time(500) and timerange.end == Time(1500)


def test_radd_int():
    """int + TimeRange -> TimeRange"""
    timerange = 500 + TimeRange(Time(1000), Time(2000))
    assert timerange.start == Time(1500) and timerange.end == Time(2500)


def test_contains_time():
    """Time in TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert Time(500) not in timerange
    assert Time(1000) in timerange
    assert Time(1500) in timerange
    assert Time(1999) in timerange
    assert Time(2000) not in timerange
    assert Time(2500) not in timerange


def test_lt_time():
    """Time < TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert Time(500) < timerange
    assert not Time(1000) < timerange
    assert not Time(1500) < timerange
    assert not Time(1999) < timerange
    assert not Time(2000) < timerange
    assert not Time(2500) < timerange


def test_le_time():
    """Time <= TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert Time(500) <= timerange
    assert Time(1000) <= timerange
    assert Time(1500) <= timerange
    assert Time(1999) <= timerange
    assert not Time(2000) <= timerange
    assert not Time(2500) <= timerange


def test_gt_time():
    """Time > TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert not Time(500) > timerange
    assert not Time(1000) > timerange
    assert not Time(1500) > timerange
    assert not Time(1999) > timerange
    assert Time(2000) > timerange
    assert Time(2500) > timerange


def test_ge_time():
    """Time >= TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert not Time(500) >= timerange
    assert Time(1000) >= timerange
    assert Time(1500) >= timerange
    assert Time(1999) >= timerange
    assert Time(2000) >= timerange
    assert Time(2500) >= timerange


def test_contains_timerange():
    """TimeRange in TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert TimeRange(Time(500), Time(800)) not in timerange
    assert TimeRange(Time(500), Time(1500)) not in timerange
    assert TimeRange(Time(1000), Time(1500)) in timerange
    assert TimeRange(Time(1200), Time(1500)) in timerange
    assert TimeRange(Time(1500), Time(2000)) in timerange
    assert TimeRange(Time(1500), Time(2500)) not in timerange
    assert TimeRange(Time(2500), Time(3000)) not in timerange


def test_lt_timerange():
    """TimeRange < TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert TimeRange(Time(500), Time(1500)) < timerange
    assert TimeRange(Time(1000), Time(1500)) < timerange
    assert not TimeRange(Time(1000), Time(2000)) < timerange
    assert not TimeRange(Time(1000), Time(2500)) < timerange
    assert not TimeRange(Time(1500), Time(2000)) < timerange


def test_le_timerange():
    """TimeRange <= TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert TimeRange(Time(500), Time(1500)) <= timerange
    assert TimeRange(Time(1000), Time(1500)) <= timerange
    assert TimeRange(Time(1000), Time(2000)) <= timerange
    assert not TimeRange(Time(1000), Time(2500)) <= timerange
    assert not TimeRange(Time(1500), Time(2000)) <= timerange


def test_eq_timerange():
    """TimeRange == TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert not TimeRange(Time(500), Time(1500)) == timerange
    assert not TimeRange(Time(1200), Time(1800)) == timerange
    assert TimeRange(Time(1000), Time(2000)) == timerange


def test_ne_timerange():
    """TimeRange != TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert TimeRange(Time(500), Time(1500)) != timerange
    assert TimeRange(Time(1200), Time(1800)) != timerange
    assert not TimeRange(Time(1000), Time(2000)) != timerange


def test_gt_timerange():
    """TimeRange > TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert not TimeRange(Time(500), Time(1500)) > timerange
    assert not TimeRange(Time(1000), Time(1500)) > timerange
    assert not TimeRange(Time(1000), Time(2000)) > timerange
    assert TimeRange(Time(1000), Time(2500)) > timerange
    assert TimeRange(Time(1500), Time(2000)) > timerange


def test_ge_timerange():
    """TimeRange >= TimeRange -> bool"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert not TimeRange(Time(500), Time(1500)) >= timerange
    assert not TimeRange(Time(1000), Time(1500)) >= timerange
    assert TimeRange(Time(1000), Time(2000)) >= timerange
    assert TimeRange(Time(1000), Time(2500)) >= timerange
    assert TimeRange(Time(1500), Time(2000)) >= timerange


def test_start():
    """TimeRange.start -> Time"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert timerange.start == Time(1000)


def test_end():
    """TimeRange.end -> Time"""
    timerange = TimeRange(Time(1000), Time(2000))
    assert timerange.end == Time(2000)
