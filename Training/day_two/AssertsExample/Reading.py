from __future__ import annotations


class SpeedReading(object):

    def __init__(self,
                 speed: int,
                 description) -> None:
        self.speed = speed
        self.description = description

    '''
    def __repr__(self):
        return f'SpeedReading({self.speed}, {self.description})'
    '''

    '''
    def __eq__(self, other: SpeedReading) -> bool:
        return self.speed == other.speed and self.description == other.description
    '''

    def __eq__(self, __value) -> bool:
        return self.speed == __value


if __name__ == '__main__':
    r1, r2 = SpeedReading(1, "one"), SpeedReading(1, "one")
    print(r1 == r2)
    # print(r1 == 1)
