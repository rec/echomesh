from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util.Reserver import Reserver
from echomesh.util.TestCase import TestCase

class ReserverTest(TestCase):
    def assertTest(self, *args):
        self.assertEqual(set(self.reserver.reserved()), set(args))

    def test_big_case(self):
        self.reserver = Reserver()
        self.assertTest()

        self.reserver.reserve(1, 2, 3)
        self.assertTest(1, 2, 3)

        self.reserver.reserve(1, 2, 3)
        self.assertTest(1, 2, 3)

        self.reserver.unreserve(1, 2)
        self.assertTest(1, 2, 3)

        self.reserver.unreserve(1)
        self.assertTest(2, 3)

        self.reserver.unreserve(2, 3)
        self.assertTest(3)

        self.reserver.unreserve(3)
        self.assertTest()

        self.reserver.reserve_uniquely(1, 2)
        self.assertTest(1, 2)

        try:
            self.reserver.reserve_uniquely(1, 2)
        except Exception as e:
            self.assertEqual(str(e), '[1, 2] are already reserved.')
        else:
            self.assertTrue(False, "Didn't get an exception")

        try:
            self.reserver.reserve(1, 2)
        except Exception as e:
            self.assertEqual(str(e), '[1, 2] are already uniquely reserved.')
        else:
            self.assertTrue(False, "Didn't get an exception")
