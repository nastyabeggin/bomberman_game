_ELEMENTS = dict(
    NONE = ' ',
    BOMBERMAN = '☺',
    BOMB_BOMBERMAN = '☻',
    DEAD_BOMBERMAN = 'Ѡ',
    OTHER_BOMBERMAN = '♥',
    OTHER_BOMB_BOMBERMAN = '♠',
    OTHER_DEAD_BOMBERMAN = '♣',
    BOMB_TIMER_5 = '5',
    BOMB_TIMER_4 = '4',
    BOMB_TIMER_3 = '3',
    BOMB_TIMER_2 = '2',
    BOMB_TIMER_1 = '1',
    BOOM = '҉',
    WALL = '☼',
    WALL_DESTROYABLE = '#',
    WALL_DESTROYED = 'H',
    MEATCHOPPER = '&',
    DEAD_MEATCHOPPER = 'x'
)

def value_of(char):
    """ Test whether the char is valid Element and return it's name."""
    for value, c in _ELEMENTS.items():
        if char == c:
            return value
    else:
        raise AttributeError("No such Element: {}".format(char))


class Element:
    """ Class describes the Element objects for Bomberman game."""

    def __init__(self, n_or_c):
        """ Construct an Element object from given name or char."""
        for n, c in _ELEMENTS.items():
            if n_or_c == n or n_or_c == c:
                self._name = n
                self._char = c
                break
        else:
            raise AttributeError("No such Element: {}".format(n_or_c))

    def get_char(self):
        """ Return the Element's character."""
        return self._char

    def __eq__(self, otherElement):
        return (self._name == otherElement._name and
                self._char == otherElement._char)


if __name__ == '__main__':
    raise RuntimeError("This module is not intended to be ran from CLI")
