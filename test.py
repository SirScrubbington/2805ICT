import unittest
import os

import ms
import cs
import main

class TestSquare(unittest.TestCase):
    def test_square_set_get_triggered(self):
        s = ms.square()
        self.assertEqual(s.get_triggered(), False)
        s.set_triggered()
        self.assertEqual(s.get_triggered(),True)

    def test_square_set_get_covered(self):
        s = ms.square()
        self.assertEqual(s.get_covered(), True)
        s.uncover()
        self.assertEqual(s.get_covered(), False)

    def test_square_get_set_bomb(self):
        s = ms.square()
        self.assertEqual(s.get_bomb(),False)
        s.set_bomb()
        self.assertEqual(s.get_bomb(),True)

    def test_square_get_set_flagged(self):
        s = ms.square()
        self.assertEqual(s.get_flagged(),False)
        s.set_flagged()
        self.assertEqual(s.get_flagged(),True)

    def test_square_get_set_adjacent(self):
        s = ms.square()
        self.assertEqual(s.get_adjacent(),0)
        for i in range(0,10):
            s.set_adjacent(i)
            self.assertEqual(s.get_adjacent(),i)

    def test_square_repr_(self):
        s=ms.square()
        print(s)

    def test_square_str_(self):
        s=ms.square()
        print(str(s))

    pass

class TestMS(unittest.TestCase):

    def test_check_solution(self):
        d = ms.generate_board(2,1)
        self.assertEqual(ms.check_solution(d),False)
        for i in d:
            for j in i:
                if j.get_bomb()==True:
                    j.set_flagged()
                else:
                    j.uncover()
        self.assertEqual(ms.check_solution(d),True)

    pass


class TestColourSquare(unittest.TestCase):
    def test_get_set_triggered(self):
        c = cs.colour_square()
        self.assertEqual(c.get_triggered(),False)
        c.set_triggered()
        self.assertEqual(c.get_triggered(),True)

    def test_get_set_covered(self):
        c = cs.colour_square()
        self.assertEqual(c.get_covered(), True)
        c.uncover()
        self.assertEqual(c.get_covered(), False)

    def test_get_set_flagged(self):
        c = cs.colour_square()
        self.assertEqual(c.get_flagged(), False)
        c.set_flagged()
        self.assertEqual(c.get_flagged(), True)

    def test_get_set_adjacent(self):
        c = cs.colour_square()
        self.assertEqual(c.get_adjacent(), 0)
        for i in range(0, 10):
            c.set_adjacent(i)
            self.assertEqual(c.get_adjacent(), i)

    def test_str_(self):
        c = cs.colour_square()
        print(str(c))

    def test_repr_(self):
        c = cs.colour_square()
        print(c)

    pass

class TestCS(unittest.TestCase):

    pass

class TestMain(unittest.TestCase):

    def test_create_db(self):
        c = main.create_db("db.db")
        self.assertNotEqual(c,None)
        c.close()
        os.remove("db.db")

    pass

    def test_insert_select_score(self):
        pass


if __name__ == '__main__':

    unittest.main()