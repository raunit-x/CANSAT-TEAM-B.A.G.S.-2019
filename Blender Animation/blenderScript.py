import bpy
import csv
import math
import random

path = "/Users/raunitsingh/Desktop/Flight_1516.csv"
dir = "/Users/raunitsingh/Desktop/bags ... cansat.STL"
count = 1
bpy.ops.import_mesh.stl(filepath=dir)
bpy.context.object.rotation_euler = (0, 0, 0)
bpy.context.object.scale = [0.01, 0.01, 0.01]
bpy.context.object.location = [-1, -1, -1.5]

with open(path) as csv_file:
    csv_read = csv.reader(csv_file)
    for i, row in enumerate (csv_read):
        if i == 0:  # Skip the first row
            continue
        pitch = math.radians(float(row[12]))  # convert degrees to radians
        roll = math.radians(float(row[13]))
        yaw = math.radians(float(random.randint(0, 180)))
        for obj in bpy.context.selected_objects:
            obj.rotation_mode = "XYZ"
            obj.rotation_euler = (pitch, yaw, roll)
            obj.keyframe_insert(data_path='rotation_euler', frame=count + 6)
        count += 6
