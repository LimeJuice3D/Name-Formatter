from .modules import name_formatter

bl_info = {
    "name": "Name Formatter",
    "description": "An object naming tool designed to format incongruous naming conventions.",
    "author": "Liam D'Arcy",
    "version": (0, 0, 1),
    "blender": (4, 5, 2),
    "category": "Rigging"
}

modules = [
    name_formatter,
]

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()
