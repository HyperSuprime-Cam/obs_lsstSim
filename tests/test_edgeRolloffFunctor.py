#
# LSST Data Management System
# Copyright 2015=2017 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
from __future__ import absolute_import, division, print_function
import sys
import unittest

import numpy as np

import lsst.obs.lsstSim as obs_lsstSim
import lsst.pex.exceptions as pexExcept
import lsst.utils.tests


def num_deriv(func, x, eps=1e-7):
    h = eps*max(abs(x), 1)
    xp = x + h
    dx = xp - x
    return (func(x + dx) - func(x))/dx


class EdgeRolloffFunctorTestCase(unittest.TestCase):
    """
    Tests for lsst.obs.lsstSim.EdgeRolloffFunctor class.
    """

    def setUp(self):
        self.funcs = [obs_lsstSim.EdgeRolloffFunctor(2, 30, 4000)]
        self.xvals = np.logspace(-8, 1, 10)
        self.y0 = 1

    def tearDown(self):
        while self.funcs:
            self.funcs.pop()

    def testDerivatives(self):
        for func in self.funcs:
            for xx in self.xvals:
                self.assertAlmostEqual(func.derivative(xx), num_deriv(func, xx), places=6)

    def testInverse(self):
        for func in self.funcs:
            for xx in self.xvals:
                yy = func(xx)
                self.assertAlmostEqual(xx, func.inverse(yy), places=6)

    def testInverseTolOutOfRangeError(self):
        maxiter = 1000
        for func in self.funcs:
            self.assertRaises(pexExcept.OutOfRangeError, func.inverse, self.y0, 10., maxiter)
            self.assertRaises(pexExcept.OutOfRangeError, func.inverse, self.y0, -1, maxiter)

    def testInverseMaxiterOutOfRangeError(self):
        tol = 1e-5
        for func in self.funcs:
            # Check bad maxiter value.
            self.assertRaises(pexExcept.OutOfRangeError, func.inverse, self.y0, tol, 0)

    def testInverseMaxiterRuntimeError(self):
        for func in self.funcs:
            # Check for exceeding maximum iterations.
            self.assertRaises(pexExcept.RuntimeError, func.inverse, self.y0, 1e-10, 1)


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    setup_module(sys.modules[__name__])
    unittest.main()
