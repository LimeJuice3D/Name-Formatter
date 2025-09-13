"""
This file is part of the Name Formatter Addon.
the Name Formatter Addon is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published 
by the Free Software Foundation, either version 3 of the License, 
or (at your option) any later version.

the Name Formatter Addon is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with the Name Formatter Addon. If not, see <https://www.gnu.org/licenses/>. 
"""

# currently only works on bones.

import bpy
from dataclasses import dataclass
from enum import Enum

PREFIX = 0
BODY = 1
SIDE = 2
NUMBER = 3
UNDEFINED = 4

@dataclass
class Segment:
    name: str = ""
    type: int = UNDEFINED

class FormatSpecifications(bpy.types.PropertyGroup):

    format_guide: bpy.props.StringProperty(
        name="Formatting Guide",
        default="Pr_BdBd#.x",
        description="Used to format your strings. use Pr for prefixes, BdBd for names, x for left/right and # for numbers. The first number, regardless of separator characters will be assumed to be a numerical segment while the rest of the numbers are ignored."
    )
    
    separator_chars: bpy.props.StringProperty(
        name="Separator Characters",
        default="-_./",
        description="Characters used to separate segments."
    )

    format_prefix: bpy.props.StringProperty(
        name="Prefix",
        default="",
        description="Any segment equal to this will be considered the prefix. There can only be one prefix so by default only the first encountered prefix will be considered while the rest are ignored. Separate prefixes using , ."
    )

class NameFormatterUI(bpy.types.Panel):
    """UI Interface for the Name Formatter"""
    bl_label = "Name Formatter"
    bl_idname = "PT_StraightUvs"
    bL_space_type = "3D"
    bl_region_type = "UI"
    bl_category = "Name Formatter"

    def draw(self, context):
        layout = self.layout

        layout.row().prop(format_specs, "format_guide")
        layout.row().prop(format_specs, "separator_chars")
        layout.row().operator(NameFormatterOp.bl_idname)

class NameFormatterOp(bpy.types.Operator):
    bl_idname = "name_formatter"
    bl_label = "Format names according to specifications"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def execute(self, context):
        NameFormatterMain(context, self)
        return {'FINISHED'}

def NameFormatterMain(context, operator):
    selected = bpy.context.selected_bones

    for b in selected:
        ReformatBone(b)

def ReformatBone(bone):
    prefix, body, number, side = ParseName(bone.name)

def ParseName(name):
    seg_arr = []
    seg = Segment()

    separators = bpy.types.Scene.format_specs.separator_chars

    for c in name:
        if c in separators:
            seg_arr.append(segment)
            seg = Segment()
        else:
            seg.name += c

    for s in seg_arr:
        s.type = DefineSegment(s)

def DefineSegment(str):
    if str in GetPrefixes():
        return PREFIX
    side_vals = ["l", "r", "L", "R"]
    if str in side_vals:
        return SIDE
    if str.is_digits():
        return NUMBER

    return BODY

def GetPrefixes():
    prefix_str = bpy.types.Scene.format_specs.format_prefix

    arr = []
    prefix = ""

    for c in prefix_str:
        if c == ',':
            arr.append(prefix)
            prefix = ""
        else:
            prefix += c

    return arr

classes = [
    FormatSpecifications, 
    NameFormatterUI,
    NameFormatterOp
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.format_specs = PointerProperty(type=FormatSpecifications)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
