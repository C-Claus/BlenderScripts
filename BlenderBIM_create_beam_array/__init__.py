# Blender Add-on Template
# Contributor(s): Aaron Powell (aaron@lunadigital.tv)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
        "name": "BIM Array Demo",
        "description": "Just an add-on",
        "author": "Coen Claus",
        "version": (1, 0),
        "blender": (3, 5, 0),
        "location": "Panel Demo",
        "warning": "", # used for warning icon and text in add-ons panel
        #"wiki_url": "http://my.wiki.url",
        #"tracker_url": "http://my.bugtracker.url",
        "support": "COMMUNITY",
        "category": "Import-Export"
        }

import bpy

#
# Add additional functions here
#
from . import  properties, ui, operator

def register():
    from . import properties
    from . import ui
    from . import operator
  
    properties.register()
    ui.register()
    operator.register()

def unregister():
    from . import properties
    from . import ui
    from . import operator

    properties.unregister()
    ui.unregister()
    operator.unregister()


if __name__ == '__main__':
    register()