#!/usr/bin/python -u
#
# Python Bindings for LZMA
#
# Copyright (c) 2004-2006 by Joachim Bauch, mail@joachim-bauch.de
# 7-Zip Copyright (C) 1999-2005 Igor Pavlov
# LZMA SDK Copyright (C) 1999-2005 Igor Pavlov
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# $Id$
#
import os
import pylzma
from py7zlib import Archive7z
import unittest

try:
    sorted
except NameError:
    # Python 2.3 and older
    def sorted(l):
        l = list(l)
        l.sort()
        return l

ROOT = os.path.abspath(os.path.split(__file__)[0])

class Test7ZipFiles(unittest.TestCase):
    
    def _test_archive(self, filename):
        fp = file(os.path.join(ROOT, 'data', filename), 'rb')
        archive = Archive7z(fp)
        self.failUnlessEqual(sorted(archive.getnames()), ['test/test2.txt', 'test1.txt'])
        self.failUnlessEqual(archive.getmember('test2.txt'), None)
        cf = archive.getmember('test1.txt')
        self.failUnlessEqual(cf.read(), 'This file is located in the root.')
        cf.reset()
        self.failUnlessEqual(cf.read(), 'This file is located in the root.')

        cf = archive.getmember('test/test2.txt')
        self.failUnlessEqual(cf.read(), 'This file is located in a folder.')
        cf.reset()
        self.failUnlessEqual(cf.read(), 'This file is located in a folder.')

    def test_non_solid(self):
        # test loading of a non-solid archive
        self._test_archive('non_solid.7z')

    def test_solid(self):
        # test loading of a solid archive
        self._test_archive('solid.7z')

def test_main():
    from test import test_support
    test_support.run_unittest(Test7ZipFiles)

if __name__ == "__main__":
    unittest.main()