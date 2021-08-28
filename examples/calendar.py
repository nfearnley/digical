from __future__ import annotations

from digical import Time, TimeRange, Schedule


class Person:
    def __init__(self, name, zone=0) -> None:
        self.name = name
        self.zone = zone
        self.schedule = Schedule()

    def add(self, time_range):
        time_range += self.zone * 60
        self.schedule.add(time_range)


def main():
    # "Test"
    person_a = Person("Digi", -5)
    person_b = Person("Natalie", -5)
    person_c = Person("Arceus", -6)

    person_a.add(TimeRange(Time.from_dhm(0, 12, 0), Time.from_dhm(0, 24, 0)))
    person_a.add(TimeRange(Time.from_dhm(1, 12, 0), Time.from_dhm(1, 24, 0)))
    person_a.add(TimeRange(Time.from_dhm(2, 12, 0), Time.from_dhm(2, 24, 0)))
    person_a.add(TimeRange(Time.from_dhm(3, 12, 0), Time.from_dhm(3, 24, 0)))
    person_a.add(TimeRange(Time.from_dhm(4, 12, 0), Time.from_dhm(4, 24, 0)))
    person_a.add(TimeRange(Time.from_dhm(5, 12, 0), Time.from_dhm(5, 24, 0)))
    person_a.add(TimeRange(Time.from_dhm(6, 12, 0), Time.from_dhm(6, 24, 0)))
    person_b.add(TimeRange(Time.from_dhm(0, 12, 0), Time.from_dhm(0, 24, 0)))
    person_b.add(TimeRange(Time.from_dhm(2, 12, 0), Time.from_dhm(2, 24, 0)))
    person_b.add(TimeRange(Time.from_dhm(4, 12, 0), Time.from_dhm(4, 24, 0)))
    person_b.add(TimeRange(Time.from_dhm(6, 12, 0), Time.from_dhm(6, 24, 0)))
    person_c.add(TimeRange(Time.from_dhm(0, 0, 0), Time.from_dhm(3, 0, 0)))

    s = person_a.schedule & person_b.schedule & person_c.schedule
    print(s)


if __name__ == "__main__":
    main()
