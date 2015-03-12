#
# Realm667 - An Awesome Awesomeness
# Copyright (C) 2015 Alexey Lysiuk
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
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import time

class Profiler(object):
    def __init__(self, enable):
        self._enable = enable

        if self._enable:
            import cProfile

            self._profiler = cProfile.Profile()
            self._profiler.enable()
        else:
            self._start_time = time.clock()

    def close(self):
        if self._enable:
            self._profiler.disable()

            import cStringIO
            import pstats

            profiling_stream = cStringIO.StringIO()
            stats = pstats.Stats(self._profiler,
                stream = profiling_stream).sort_stats('cumulative')
            stats.print_stats()

            print('\n')
            print(profiling_stream.getvalue())
        else:
            build_time = time.clock() - self._start_time
            print('Completed in {0:.3f} seconds'.format(build_time))