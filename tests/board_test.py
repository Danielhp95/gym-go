import unittest

from go import Board, BoardError


class BoardTest(unittest.TestCase):
    """
    Won't test any of the array functionality.  That is covered in
    array_test.py.
    """

    def setUp(self):
        self.bo = Board(5)

    def test_init(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo._array, [
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
        ])

        self.assertTrue(self.bo._turn is b)
        self.assertEqual(self.bo._score, {b: 0, w: 0})
        self.assertEqual(self.bo._history, [])
        self.assertEqual(self.bo._redo, [])

    def test_turn(self):
        self.assertEqual(self.bo.turn, 'Black')
        self.bo.move(1, 1)
        self.assertEqual(self.bo.turn, 'White')
        self.bo.move(2, 2)
        self.assertEqual(self.bo.turn, 'Black')
        self.bo.move(3, 3)
        self.assertEqual(self.bo.turn, 'White')

    def test_score(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo.score, {
            'black': 0,
            'white': 0,
        })

        self.bo._array = [
            [w, b, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
            [e, e, e, e, e],
        ]
        self.bo.move(1, 2)

        self.assertEqual(self.bo.score, {
            'black': 1,
            'white': 0,
        })

        self.setUp()
        self.bo._array = [
            [w, b, e, e, e],
            [w, b, e, e, e],
            [e, w, b, e, e],
            [w, b, e, e, e],
            [b, e, e, e, e],
        ]
        self.bo.move(1, 3)

        self.assertEqual(self.bo.score, {
            'black': 4,
            'white': 0,
        })

    def test_next_turn(self):
        b = Board.BLACK
        w = Board.WHITE

        self.assertTrue(self.bo._next_turn is w)
        self.bo.move(1, 1)
        self.assertTrue(self.bo._next_turn is b)
        self.bo.move(2, 2)
        self.assertTrue(self.bo._next_turn is w)
        self.bo.move(3, 3)
        self.assertTrue(self.bo._next_turn is b)

    def test_flip_turn(self):
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo._turn, b)
        self.bo._flip_turn()
        self.assertEqual(self.bo._turn, w)
        self.bo._flip_turn()
        self.assertEqual(self.bo._turn, b)
        self.bo._flip_turn()
        self.assertEqual(self.bo._turn, w)

    def test_state(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        state = (
            [
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
            ],
            b,
            {
                b: 0,
                w: 0,
            },
        )
        _state = self.bo._state

        self.assertEqual(_state[0], state[0])
        self.assertEqual(_state[1], state[1])
        self.assertEqual(_state[2], state[2])

        self.assertTrue(_state[0] is not state[0])
        self.assertTrue(_state[1] is state[1])
        self.assertTrue(_state[2] is not state[2])

        self.bo.move(3, 3)

        state = (
            [
                [e, e, e, e, e],
                [e, e, e, e, e],
                [e, e, b, e, e],
                [e, e, e, e, e],
                [e, e, e, e, e],
            ],
            w,
            {
                b: 0,
                w: 0,
            },
        )
        _state = self.bo._state

        self.assertEqual(_state[0], state[0])
        self.assertEqual(_state[1], state[1])
        self.assertEqual(_state[2], state[2])

        self.assertTrue(_state[0] is not state[0])
        self.assertTrue(_state[1] is state[1])
        self.assertTrue(_state[2] is not state[2])

    def test_load_state(self):
        state = self.bo._state

        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state)

        self.bo._load_state(state)

        self.assertEqual(self.bo._state, state)

    def test_push_history(self):
        self.assertEqual(self.bo._history, [])

        state = self.bo._state

        self.bo._push_history()

        self.assertTrue(len(self.bo._history) == 1)
        self.assertEqual(self.bo._history[0], state)

    def test_pop_history(self):
        self.assertEqual(self.bo._history, [])

        state = self.bo._state
        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state)

        self.bo._pop_history()

        self.assertEqual(self.bo._state, state)

    def test_undo(self):
        self.assertRaises(BoardError, self.bo.undo)
        self.assertEqual(self.bo._redo, [])
        self.assertEqual(self.bo._history, [])

        state1 = self.bo._state
        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state1)
        self.assertEqual(self.bo._history, [state1])
        self.assertEqual(self.bo._redo, [])

        state2 = self.bo._state
        pop_state = self.bo.undo()

        self.assertEqual(self.bo._state, state1)
        self.assertEqual(pop_state, state2)
        self.assertNotEqual(self.bo._state, pop_state)

        self.assertEqual(self.bo._history, [])
        self.assertEqual(self.bo._redo, [pop_state])

    def test_redo(self):
        self.assertRaises(BoardError, self.bo.undo)
        self.assertEqual(self.bo._redo, [])
        self.assertEqual(self.bo._history, [])

        state1 = self.bo._state
        self.bo.move(3, 3)

        self.assertNotEqual(self.bo._state, state1)
        self.assertEqual(self.bo._history, [state1])
        self.assertEqual(self.bo._redo, [])

        state2 = self.bo._state
        pop_state = self.bo.undo()

        self.assertEqual(self.bo._state, state1)
        self.assertEqual(pop_state, state2)
        self.assertNotEqual(self.bo._state, pop_state)

        self.assertEqual(self.bo._history, [])
        self.assertEqual(self.bo._redo, [pop_state])

        self.bo.redo()

        self.assertEqual(self.bo._state, state2)
        self.assertNotEqual(self.bo._state, state1)
        self.assertEqual(self.bo._history, [state1])
        self.assertEqual(self.bo._redo, [])

    def test_tally(self):
        self.assertEqual(self.bo.score, {
            'black': 0,
            'white': 0,
        })

        self.bo._tally(100)

        self.assertEqual(self.bo.score, {
            'black': 100,
            'white': 0,
        })

        self.bo.move(3, 3)
        self.bo._tally(100)

        self.assertEqual(self.bo.score, {
            'black': 100,
            'white': 100,
        })

    def test_get_none(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertTrue(self.bo._get_none(1, 1) is e)
        self.bo.move(3, 3)
        self.assertTrue(self.bo._get_none(3, 3) is b)
        self.bo.move(3, 2)
        self.assertTrue(self.bo._get_none(3, 2) is w)
        self.assertTrue(self.bo._get_none(-1, 100) is None)

    def test_get_surrounding(self):
        e = Board.EMPTY
        b = Board.BLACK
        w = Board.WHITE

        self.assertEqual(self.bo._get_surrounding(3, 3), [
            (e, (3, 2)),
            (e, (4, 3)),
            (e, (3, 4)),
            (e, (2, 3)),
        ])

        self.bo.move(1, 1)

        self.assertEqual(self.bo._get_surrounding(2, 1), [
            (e, (3, 1)),
            (e, (2, 2)),
            (b, (1, 1)),
        ])

        self.bo.move(2, 1)

        self.assertEqual(self.bo._get_surrounding(1, 1), [
            (w, (2, 1)),
            (e, (1, 2)),
        ])
        self.assertEqual(self.bo._get_surrounding(5, 5), [
            (e, (5, 4)),
            (e, (4, 5)),
        ])
