from digical import Time


def test_init():
    """Time(int) -> Time"""
    time = Time(1563)
    assert time is not None


def test_from_dhm():
    """Time.from_dhm(int, int, int) -> Time"""
    time = Time.from_dhm(1, 2, 3)
    assert time is not None
    assert time.value == 1563


def test_from_json():
    """Time.from_json(dict) -> Time"""
    time = Time.from_json({"value": 1563})
    assert time.value == 1563


def test_to_json():
    """Time.to_json() -> dict"""
    time_json = Time(1563).to_json()
    assert time_json["value"] == 1563


def test_copy():
    """Time.copy() -> Time"""
    time_a = Time(0)
    time_b = time_a.copy()
    assert time_a == time_b
    assert time_a is not time_b


def test_hash():
    """hash(TimeRange) -> int"""
    time = Time(1563)
    assert isinstance(hash(time), int)


def test_repr():
    """repr(Time) -> str"""
    time = Time(1563)
    assert repr(time) == "Time(1563)"


def test_str():
    """str(Time) -> str"""
    time = Time(1563)
    assert str(time) == "Monday, 2:03"


def test_value():
    """Time.value -> int"""
    time = Time(1563)
    assert time.value == 1563


def test_weekday():
    """Time.weekday -> int"""
    time = Time(1563)
    assert time.weekday == 1


def test_day():
    """Time.day -> int"""
    time = Time(1563)
    assert time.day == 1


def test_hour():
    """Time.hour -> int"""
    time = Time(1563)
    assert time.hour == 2


def test_minute():
    """Time.minute -> int"""
    time = Time(1563)
    assert time.minute == 3


def test_dayname():
    """Time.dayname -> str"""
    time = Time(1563)
    assert time.dayname == "Monday"


def test_eq():
    """Time == Time -> bool"""
    time_a = Time(100)
    time_b = Time(100)
    time_c = Time(110)
    assert time_a == time_b
    assert not (time_a == time_c)


def test_ne():
    """Time != Time -> bool"""
    time_a = Time(100)
    time_b = Time(100)
    time_c = Time(110)
    assert not (time_a != time_b)
    assert time_a != time_c


def test_lt():
    """Time < Time -> bool"""
    time_a = Time(100)
    time_b = Time(110)
    assert time_a < time_b
    assert not (time_b < time_a)


def test_le():
    """Time <= Time -> bool"""
    time_a = Time(100)
    time_b = Time(100)
    time_c = Time(110)
    assert time_a <= time_b
    assert time_a <= time_c
    assert not(time_c <= time_a)


def test_gt():
    """Time > Time -> bool"""
    time_a = Time(100)
    time_b = Time(110)
    assert time_b > time_a
    assert not (time_a > time_b)


def test_ge():
    """Time >= Time -> bool"""
    time_a = Time(100)
    time_b = Time(100)
    time_c = Time(110)
    assert time_b >= time_a
    assert time_c >= time_a
    assert not(time_a >= time_c)


def test_add_int():
    """Time + int -> Time"""
    time = Time(100) + 10
    assert time.value == 110


def test_radd_int():
    """int + Time -> Time"""
    time = 10 + Time(100)
    assert time.value == 110


def test_sub_int():
    """Time - int -> Time"""
    time = Time(100) - 10
    assert time.value == 90


def test_sub_time():
    """Time - Time -> int"""
    minutes = Time(120) - Time(100)
    assert minutes == 20
