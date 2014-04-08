# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "oenvoyage Toolset",
    "author": "Olivier Amrein",
    "version": (0, 1, 0),
    "blender": (2, 70),
    "location": "Everywhere!",
    "description": "A collection of tools and settings to improve productivity (based on Amaranth)",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Scene"}


import bpy
from bpy.types import Operator, AddonPreferences, Panel, Menu
from bpy.props import BoolProperty
from datetime import datetime, timedelta

# Preferences
class OenvoyageToolsetPreferences(AddonPreferences):
    bl_idname = __name__
    use_render_estimate = BoolProperty(
            name="Estimate Render time",
            description="blalblalabl 3D View",
            default=True,
            )

    def draw(self, context):
        layout = self.layout

        layout.label(
            text="Here you can enable or disable specific tools, "
                 "in case they interfere with others or are just plain annoying")

        split = layout.split(percentage=0.25)

        col = split.column()
        sub = col.column(align=True)
        sub.label(text="Render Options", icon="RENDER_STILL")
        sub.prop(self, "use_render_estimate")

# Properties
def init_properties():

    scene = bpy.types.Scene
    
    scene.average_rendertime = bpy.props.FloatProperty(min=0, default=5, max = 200)

def clear_properties():
    props = (
        "use_render_estimate",
    )
    
    wm = bpy.context.window_manager
    for p in props:
        if p in wm:
            del wm[p]


# FEATURE: Estimate Time to Render an Animation
def hours_float_to_str(rendertime): 
    hours_int = int(rendertime)
    left_mins = (rendertime - hours_int)*60
    if left_mins > 0:
        return "%d:%02d" % (hours_int,left_mins)
    else:
        return hours_int
 
def estimate_render_animation_time(self, context):
    preferences = context.user_preferences.addons[__name__].preferences
    
    if preferences.use_render_estimate:
        layout = self.layout
        scene = context.scene
            
        total_frames = scene.frame_end - scene.frame_start
        
        avg = scene.average_rendertime 
        estimated_rendertime = total_frames * avg/60

        rendertime_in_hours = hours_float_to_str(estimated_rendertime)
        
        estimated_finish_time = datetime.now() + timedelta(hours=estimated_rendertime)
        formatted_finish_time = '{:%a, %d %b @ %H:%M}'.format(estimated_finish_time)

        row = layout.row()
        split =layout.split()
        split.label("Average rendertime: ")
        
        split.prop(scene,"average_rendertime", text="mins")

        row = layout.row()
        row = row.label("Expected rendertime for %s frames is:"  % total_frames)
        row = layout.row()
        row = row.label("%s hours (ETA %s)"  % (rendertime_in_hours,formatted_finish_time))
# // FEATURE: Estimate Time to Render an Animation

# FEATURE: Motion paths buttons in W special key
def motion_path_buttons(self, context):

    obj = context.active_object
    scene = context.scene

    self.layout.separator()
    if obj.motion_path:
        self.layout.operator("object.paths_update", text="Update Object Paths")
        self.layout.operator("object.paths_clear", text="Clear Object Paths")
    else:
        self.layout.operator("object.paths_calculate", text="Calculate Object Paths")
    
# // FEATURE: Motion paths buttons in W

addon_keymaps = []

def register():

    bpy.utils.register_class(OenvoyageToolsetPreferences)

    init_properties()
    # UI: Register the panel

    bpy.types.RENDER_PT_render.append(estimate_render_animation_time)
    bpy.types.VIEW3D_MT_object_specials.append(motion_path_buttons)

def unregister():

    bpy.utils.unregister_class(OenvoyageToolsetPreferences)

    bpy.types.RENDER_PT_render.remove(estimate_render_animation_time)
    bpy.types.VIEW3D_MT_object_specials.remove(motion_path_buttons)
    
    clear_properties()

if __name__ == "__main__":
    register()