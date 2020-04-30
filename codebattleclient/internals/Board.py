from math import sqrt

from codebattleclient.internals.Element import Element
from codebattleclient.internals.Point import Point


class Board:
    """ Class describes the Board field for Bomberman game."""

    def __init__(self, board_string):
        self._string = board_string.replace('\n', '')
        self._len = len(self._string)  # the length of the string
        self._size = int(sqrt(self._len))  # size of the board

    def get_bomberman(self):
        return self.find_first_element(Element('BOMBERMAN'), Element('DEAD_BOMBERMAN'), Element('BOMB_BOMBERMAN'))

    def get_other_bombermans(self):
        return self._find_all(Element('OTHER_BOMBERMAN'), Element('OTHER_DEAD_BOMBERMAN'), Element('OTHER_BOMB_BOMBERMAN'))

    def get_walls(self):
        return self._find_all(Element('WALL'))

    def am_i_dead(self):
        return self.find_first_element(Element('DEAD_BOMBERMAN')) is not None


    def get_destroyable_walls(self):
        return self._find_all(Element('WALL_DESTROYABLE'))

    def get_metchoppers(self):
        return self._find_all(Element('MEATCHOPPER'))

    def get_blasts(self):
        return self._find_all(Element('BOOM'))

    def get_bombs(self):
        """ Return the list of bombs Points."""
        points = set()
        points.update(self._find_all(Element('BOMB_BOMBERMAN'), Element('BOMB_TIMER_1'), Element('BOMB_TIMER_2'),
                                     Element('BOMB_TIMER_5'), Element('BOMB_TIMER_4'), Element('BOMB_TIMER_3')))
        return list(points)

    def get_barriers(self):
        """ Return the list of barriers Points."""
        points = set()
        points.update(self._find_all(Element('MEATCHOPPER'), 
                                     Element('WALL'), Element('WALL_DESTROYABLE'),
                                     Element('OTHER_BOMBERMAN'), Element('OTHER_BOMB_BOMBERMAN'),
                                     Element('BOMB_TIMER_1'), Element('BOMB_TIMER_2'), Element('BOMB_TIMER_3'), Element('BOMB_TIMER_4'), Element('BOMB_TIMER_5')))
        return list(points)

    def get_point_by_shift(self, shift):
        return Point(shift % self._size, shift / self._size)

    def find_first_element(self, *element_types):
        _result = []
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            for type in element_types:
                if self.has_element_at(point, type):
                    return point
        return None

    def _find_all(self, *element_types):
        """ Returns the list of points for the given element type."""
        _points = []
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            for type in element_types:
                if self.has_element_at(point, type):
                    _points.append(point)
        return _points

    def is_barrier_at(self, point):
        return self.get_barriers().__contains__(point)

    def get_element_at(self, point):
        """ Return an Element object at coordinates x,y."""
        return Element(self._string[self._xy2strpos(point.get_x(), point.get_y())])

    def has_element_at(self, point, element_object):
        if point.is_out_of_board(self._size):
            return False
        return element_object == self.get_element_at(point)

    def find_element(self, type):
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            if self.has_element_at(point, type):
                return point
        return None

    def get_shift_by_point(self, point):
        return point.get_y() * self._size + point.get_x()

    def _strpos2pt(self, strpos):
        return Point(*self._strpos2xy(strpos))

    def _strpos2xy(self, strpos):
        return (strpos % self._size, strpos // self._size)

    def _xy2strpos(self, x, y):
        return self._size * y + x

    def print_board(self):
        print(self._line_by_line())

    def _line_by_line(self):
        return '\n'.join([self._string[i:i + self._size]
                          for i in range(0, self._len, self._size)])

    def to_string(self):
        return ("Board:\n{brd}".format(brd=self._line_by_line()))

    #def is_free(self):
    def is_free(self, point):
        if point.is_out_of_board(self._size):
            return False
        if self._find_all(Element('NONE'), Element('DEAD_MEATCHOPPER'), Element('OTHER_DEAD_BOMBERMAN')).__contains__(point):
            return True
        return False

    def get_fast_bombs(self, ind=2):
        """ Return the list of bombs Points."""
        points = set()
        el = [Element('BOMB_TIMER_{}'.format(i)) for i in range(1, ind)]
        points.update(self._find_all(*el))
        return list(points)


    def get_the_nearest_bomberman(self):
        all_bombermen = self._find_all(Element('OTHER_BOMBERMAN'))
        my_point = self.get_bomberman()
        mx, my = my_point.get_x(), my_point.get_y()
        print(mx, my)
        d = {}
        for i in all_bombermen:
            x, y = i.get_x(), i.get_y()
            d[i] = int(sqrt((mx - x) ** 2 + (my - y) ** 2))
        return min(d, key=d.get)







if __name__ == '__main__':
    raise RuntimeError("This module is not designed to be ran from CLI")
