# doomwad.py: Doom WAD file library
#
# Copyright (c) 2009 Jared Stafford (jspenguin@gmail.com)
# Copyright (c) 2015 Alexey Lysiuk
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Read and write Doom WAD files"""

import md5
import string
import struct
from cStringIO import StringIO

_spriteanglechar = string.digits + string.ascii_uppercase[:7]

_header = struct.Struct("<4sII")
_dirent = struct.Struct("<II8s")

# Map members
specnames = set(('THINGS', 'VERTEXES','LINEDEFS', 'SIDEDEFS', 'SEGS',
                 'SSECTORS', 'NODES', 'SECTORS', 'REJECT', 'BLOCKMAP',
                 'BEHAVIOR', 'SCRIPTS'))

spritemarker = 'S_START'

def issrpitenamespace(namespace):
    return namespace == spritemarker or namespace[1:] == spritemarker

def issequentialsprite(name):
    if name.startswith('ARTI'):
        # The very special case for Heretic and Hexen
        # This is a non-sequential sprite
        return False
    else:
        size = len(name)

        # 6th and 8th characters represent sprite angles
        angle1 = 6 == size and name[5] in _spriteanglechar
        angle2 = 8 == size and name[5] in _spriteanglechar \
                           and name[7] in _spriteanglechar

        # Treat a sprite is a part of the sequence
        # if its name contains one or two valid angle characters
        return angle1 or angle2

class Lump(object):
    def __init__(self, name, data, index=None):
        self.name = name
        self.data = data
        self.index = index
        self.marker = data == "" and name not in specnames
        self.namespace = ''

    def hash(self):
        result = md5.new()
        result.update(self.data)
        return result.digest()

class WadFile(object):
    def __init__(self, data_or_file):
        if hasattr(data_or_file, 'read') and \
                hasattr(data_or_file, 'seek'):
            file = data_or_file
        else:
            file = StringIO(data_or_file)

        self.filename = hasattr(file, 'name') and file.name or ''

        sig, numentries, offset = _header.unpack(file.read(12))

        if (sig != 'IWAD' and sig != 'PWAD'):
            raise ValueError('not a WAD file')

        self.sig = sig

        file.seek(offset, 0)
        direct = file.read(16 * numentries)

        lumps = []

        for i in xrange(numentries):
            pos = i * 16
            offset, size, name = _dirent.unpack(direct[pos : pos + 16])
            idx = name.find('\0')
            if idx != -1:
                name = name[:idx]

            if size:
                file.seek(offset, 0)
                data = file.read(size)
            else:
                data = ""

            lumps.append(Lump(name.upper(), data, i))

        self.lumps = lumps
        self._assignnamespaces()

    def _assignnamespaces(self):
        namespace = ''
        ismap = False

        for lump in self:
            ismapcur = lump.name in specnames

            if lump.marker:
                if lump.name.endswith('_END'):
                    namespace = ''
                else:
                    namespace =  lump.name
                ismap = False
            else:
                if not ismapcur and ismap:
                    namespace = ''
                    ismap = False

                lump.namespace = namespace

            ismap = ismapcur

    def writeto(self, file):
        directory = []
        dirsize = 16 * len(self)

        pos = 12

        for lump in self:
            lsize = len(lump.data)
            directory.append((lump.name, pos, lsize))
            pos += lsize

        file.write(_header.pack(self.sig, len(self), pos))
        for lump in self:
            file.write(lump.data)

        for name, pos, size in directory:
            file.write(_dirent.pack(pos, size, name))

    # Simple linear search works fine: there are usually
    # only a few hundred lumps in a file.
    def find(self, name, marker=None):
        idx = 0
        if marker:
            idx = marker.index + 1

        name = name.upper()
        end = len(self.lumps)
        while idx < end:
            lump = self.lumps[idx]
            if lump.name == name:
                return lump

            # Is this another marker lump?
            if marker and lump.marker:
                return None
            idx += 1
        return None

    def findmarker(self, lump):
        idx = lump.index
        while idx >= 0:
            lump = self.lumps[idx]
            if lump.marker:
                return lump

            idx -= 1
        return None

    def _reindex(self, start=0):
        for i in xrange(start, len(self.lumps)):
            self.lumps[i].index = i

    def removelump(self, lump):
       idx = lump.index
       self.lumps.remove(lump)
       self._reindex(idx)

    def insert(self, lump, before=None):
        idx = (before.index if before else len(self.lumps))
        lump.index = idx
        self.lumps.insert(idx, lump)
        self._reindex(idx + 1)

    def append(self, lump):
        self.insert(lump)

    def __getitem__(self, name):
        if isinstance(name, int):
            return self.lumps[name]

        names = name.split('/')
        lump = None
        for n in names:
            lump = self.find(n, lump)
        return lump

    def __len__(self):
        return len(self.lumps)

    def __iter__(self):
        return iter(self.lumps)

    def namespaces(self):
        """ Return sorted list of namespace names.
            Namespace is named by its start marker.
            An empty string designates the global namespace """
        namespaces = set()

        for lump in self:
            if lump.namespace not in namespaces:
                namespaces.add(lump.namespace)

        return sorted(namespaces)

    def namespacelumps(self, namespace):
        """ Return list of lumps belong to a namespace with the given name
            lumps ordering is preserved and duplicates are included """
        lumps = []

        for lump in self:
            if lump.namespace == namespace:
                lumps.append(lump)

        return lumps

    def uniquenamespacelumps(self, namespace):
        """ Return list of lumps belong to a namespace with the given name
            lumps ordering is preserved and duplicates are removed """
        lumps = []
        names = set()

        for lump in self.namespacelumps(namespace):
            if lump.name not in names:
                lumps.append(lump)
                names.add(lump.name)

        return lumps

    def spritelumps(self):
        """ Return list of sprite lumps """
        lumps = []

        for lump in self:
            if issrpitenamespace(lump.namespace):
                lumps.append(lump)

        return lumps

    def spritenames(self):
        """ Return sorted list of sprite names """
        names = set()

        for lump in self.spritelumps():
            name = lump.name
            names.add(issequentialsprite(name) and name[:4] or name)

        return sorted(names)

    def spritemapping(self):
        """
        Return dictionary with sprite/frame mapping with format:
        { sprite: { frame: hash,
                    frame: hash,
                    ... },
          sprite: { ... },
          ... }
        """
        result = { }

        for lump in self.spritelumps():
            lumpname = lump.name
            lumphash = lump.hash()

            if issequentialsprite(lumpname):
                name  = lumpname[:4]
                frame = lumpname[4:]

                if name in result:
                    result[name][frame] = lumphash
                else:
                    result[name] = { frame: lumphash }
            else:
                result[lumpname] = { lumpname: lumphash }

        return result

    def filter(self, function):
        """ Keep only those lumps which function returns true """
        self.lumps = filter(function, self)
        self._reindex()

    def removesprite(self, sprite):
        """ Remove sprite lumps by sprite name """
        def should_keep_lump(lump):
            return not issrpitenamespace(lump.namespace) \
                or not lump.name.startswith(sprite)

        self.filter(should_keep_lump)

parsers = {}

def readarray(stream, clas):
    if isinstance(stream, Lump):
        stream = stream.data

    if isinstance(stream, str):
        stream = StringIO(stream)

    ret = []
    ssize = clas.size
    while True:
        dat = stream.read(ssize)
        if len(dat) < ssize:
            break

        ret.append(clas.fromstr(dat))
    return ret

def writearray(stream, array):
    for item in array:
        stream.write(str(item))

def _defparser(name, sdef, *members):
    mstruct = struct.Struct(sdef)
    class clas(object):
        size = mstruct.size


        def __init__(self, *args, **kwargs):
            for i, v in enumerate(args):
                setattr(self, members[i], v)

            for k, v in kwargs.items():
                setattr(self, k, v)

        def _toseq(self):
            return [getattr(self, n) for n in members]

        def __str__(self):
            return mstruct.pack(*self._toseq())

        def __repr__(self):
            return '%s(%s)' % (name, ', '.join('%s=%r' % (n, getattr(self, n))
                                               for n in members))

        @staticmethod
        def fromstr(string):
            return clas(*mstruct.unpack(string[:mstruct.size]))

    clas.members = members
    clas.__name__ = name
    globals()[name] = clas

# TODO: finish other structures
_defparser('Vertex', '<hh', 'x', 'y')
_defparser('Thing', '<hhhhH', 'x', 'y', 'angle', 'type', 'flags')
_defparser('HexThing', '<hhhhhhHBBBBBB', 'id', 'x', 'y', 'height',
           'angle', 'type', 'flags', 'special', 'arg0', 'arg1',
           'arg2', 'arg3', 'arg4')
_defparser('Linedef', '<HHHHHhh', 'start_vtx', 'end_vtx', 'flags',
           'special', 'sector_tag', 'right_sdef', 'left_sdef')
_defparser('HexLinedef', '<HHHBBBBBBhh', 'start_vtx', 'end_vtx',
           'flags', 'special', 'arg0', 'arg1', 'arg2', 'arg3',
           'arg4', 'right_sdef', 'left_sdef')


if __name__ == '__main__':
    import sys

    if 1 == len(sys.argv):
        print('Usage: {0} file.wad ...'.format(__file__))
        exit(1)

    allsprites = { }

    for filename in sys.argv[1:]:
        wad_file = open(filename, 'rb')
        wad_data = wad_file.read()
        wad_file.close()

        wad = WadFile(wad_data)

        for name, frames in wad.spritemapping().iteritems():
            if name in allsprites:
                template = allsprites[name] == frames                 \
                    and '[.] Identical sprite {0} was found'          \
                    or  '[!] Sprite collision for name {0} was found'
                print(template.format(name))
            else:
                allsprites[name] = frames

##    from pprint import pprint
##    pprint(allsprites)
