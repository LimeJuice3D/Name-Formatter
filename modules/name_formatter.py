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
        name="Potential Prefixes",
        default="Def,Ctrl",
        description="Include any possible prefix values here. Any segment equal to this will be considered the prefix. There can only be one prefix so by default only the first encountered prefix will be considered while the rest are ignored. Separate prefixes using a comma. ."
    )

    include_prefix: bpy.props.BoolProperty(
        name="Include Prefixes",
        default=True,
        description="Choose whether or not to include a prefix in the final result."
    )

    format_side: bpy.props.StringProperty(
        name="Potential Sides",
        default="l,r,L,R",
        description="Potential side values, typically used for rigging symmetry. Only the first side segment will be considered. Separating values using a comma."
    )

    include_side: bpy.props.BoolProperty(
        name="Include Side",
        default=True,
        description="Choose whether to include a side segment in your naming convention."
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
        layout.row().prop(format_specs, "format_prefix")
        layout.row().prop(format_specs, "include_prefix")
        layout.row().prop(format_specs, "format_side")
        layout.row().prop(format_specs, "include_side")
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
    prefix, name_arr, side, num = ParseName(bone.name)
    bone.name = ConstructName(prefix, name_arr, side, num)

def ConstructName(prefix, name_arr, side, num):
    guide = bpy.types.Scene.format_specs.format_guide

    new = guide
    new = ReplacePrefix(new, prefix)
    new = ReplaceNames(new, name_arr)

def ReplaceNames(guide, name_arr):
    pos = guide.upper().find("BDBD")
    guide_prefix = guide[pos] + guide[pos + 1]


def ReplacePrefix(guide, prefix):
    pos = guide.upper().find("PR")
    guide_prefix = guide[pos] + guide[pos + 1]

    if guide_prefix == "pr":
        case_prefix = prefix.lower()
    elif guide_prefix == "PR":
        case_prefix = prefix.upper()
    elif guide_prefix == "Pr":
        case_prefix = prefix.lower()
        case_prefix[0] = case_prefix[0].upper()
    elif guide_prefix == "pR":
        case_prefix = prefix.upper()
        case_prefix[0] = case_prefix[0].lower()

    guide[pos] = "P"
    guide[pos+1] = "R"

    return guide.replace("PR", case_prefix)

def ParseName(name):
    name_arr = []
    prefix = ""
    side = ""
    num = -1

    fspecs = bpy.types.Scene.format_specs
    separators = fspecs.separator_chars
    potential_prefixes = fspecs.format_prefix.split(",")
    potential_sides = fspecs.format_side.split(",")

    s = ""

    for c in name:
        if c in separators:
            if s in potential_prefixes:
                prefix = s
            elif s in potential_sides:
                side = s
            elif s.is_digits():
                num = s
            else:
                name_arr.append(s)

            s = ""
        else:
            s += c

    return prefix, name_arr, side, num

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
