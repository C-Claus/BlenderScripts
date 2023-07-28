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

import bpy
from bpy.types import Scene

# For more information about Blender Properties, visit:
# <https://blender.org/api/blender_python_api_2_78a_release/bpy.types.Property.html>
from bpy.props import BoolProperty
# from bpy.props import CollectionProperty
# from bpy.props import EnumProperty
# from bpy.props import FloatProperty
# from bpy.props import IntProperty
# from bpy.props import PointerProperty
# from bpy.props import StringProperty
# from bpy.props import PropertyGroup

#
# Add additional functions or classes here
#

# This is where you assign any variables you need in your script. Note that they
# won't always be assigned to the Scene object but it's a good place to start.

import bpy
from bpy.types import Scene
from bpy.props import BoolProperty
from bpy.props import FloatProperty
from bpy.props import IntProperty


class ImageItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name         ="Property",
                                   description  ="Use the PropertySet name and Property name divided by a .",
                                   default      ="PropertySet.Property"
                                   )


def register():
    bpy.utils.register_class(ImageItem)


def unregister():
    bpy.utils.unregister_class(ImageItem)
 
