#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.5.0 with dump python functionality
###

import sys
import salome
import json
salome.salome_init()
import salome_notebook
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
import  SMESH
from salome.smesh import smeshBuilder


notebook = salome_notebook.NoteBook()
param_path = sys.argv[1]

with open(param_path) as file:
    # Load its content and make a new dictionary
    parameters = json.load(file)

sys.path.append(parameters['lib_path'])


from AdditinalFiles.MeshScripts.exportMesh import export_to_foam

### GEOMETRY ###

d = parameters['d'] # diameter of obstacle
betta = parameters['betta']
h = d / betta # z - size of the duct, widht
a = h # y - size of the duct, height
Lu = 12 * d # upstream distance
Ld = 42 * d # downstream distance

### MESH ###
nIO = parameters['nIO'] # точек на входе и выходе
nC = parameters['nC']  # точек на дуге окружности
nL = parameters['nL']  # точек по длине канала
Ha = parameters['Ha']
delta_Ha = a / Ha
delta_Sh  = a / Ha ** 0.5
wall_layer = delta_Sh
circle_layer = parameters['circle_layer']
nWall_layer = parameters['nWall_layer']
nCircle_layer = parameters['nCircle_layer']
k_wall = parameters['k_wall']


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

center_dist = geompy.MakeVertex(0, 0, 0)
point1_rect = geompy.MakeVertex(-Lu, -h/2, 0)
point2_rect = geompy.MakeVertex(-Lu, h/2, 0)

#Creation of duct
edge1_rect = geompy.MakeLineTwoPnt(point1_rect, point2_rect)
edge1_rect_vertex_2 = geompy.GetSubShape(edge1_rect, [2])
rect_2d = geompy.MakePrismVecH(edge1_rect, OX, Ld)

#Creation of obstacle
obstacle_2d = geompy.MakeDiskPntVecR(center_dist, OZ, d/2)
diff_obstacle_2d = geompy.MakeCutList(rect_2d, [obstacle_2d], True)



#Geometry groups

circle_edge = geompy.CreateGroup(diff_obstacle_2d, geompy.ShapeType["EDGE"])
geompy.UnionIDs(circle_edge, [12])
walls_edge = geompy.CreateGroup(diff_obstacle_2d, geompy.ShapeType["EDGE"])
geompy.UnionIDs(walls_edge, [10, 3])
inlet_edge = geompy.CreateGroup(diff_obstacle_2d, geompy.ShapeType["EDGE"])
geompy.UnionIDs(inlet_edge, [6])
outlet_edge = geompy.CreateGroup(diff_obstacle_2d, geompy.ShapeType["EDGE"])
geompy.UnionIDs(outlet_edge, [8])

group_IO = geompy.CreateGroup(diff_obstacle_2d, geompy.ShapeType["EDGE"])
geompy.UnionList(group_IO, [inlet_edge, outlet_edge])


#Add to study
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( point1_rect, 'point1_rect' )
geompy.addToStudy( point2_rect, 'point2_rect' )
geompy.addToStudy( edge1_rect, 'edge1_rect' )
geompy.addToStudy( rect_2d, 'rect_2d' )
geompy.addToStudy( center_dist, 'center_dist' )
geompy.addToStudy( obstacle_2d, 'obstacle_2d' )
geompy.addToStudyInFather( edge1_rect, edge1_rect_vertex_2, 'edge1_rect:vertex_2' )
geompy.addToStudy( diff_obstacle_2d, 'final geometry' )
geompy.addToStudyInFather( diff_obstacle_2d, circle_edge, 'circle_edge' )
geompy.addToStudyInFather( diff_obstacle_2d, walls_edge, 'walls_edge' )
geompy.addToStudyInFather( diff_obstacle_2d, inlet_edge, 'inlet_edge' )
geompy.addToStudyInFather( diff_obstacle_2d, outlet_edge, 'outlet_edge' )
geompy.addToStudyInFather( diff_obstacle_2d, group_IO, 'group_IO' )



###
### SMESH component
###

max_size_elem = parameters['max_size_elem']
length_elem = max_size_elem
min_size_elem = parameters['min_size_elem']
k_global = parameters['k_global']
quad_elem = parameters['quad_elem']

smesh = smeshBuilder.New()

  
Mesh_2D = smesh.Mesh(diff_obstacle_2d)
NETGEN_2D = Mesh_2D.Triangle(algo=smeshBuilder.NETGEN_2D)


NETGEN_2D_Parameters = NETGEN_2D.Parameters()
NETGEN_2D_Parameters.SetMaxSize(max_size_elem)
NETGEN_2D_Parameters.SetMinSize(min_size_elem)
NETGEN_2D_Parameters.SetFineness(5)
NETGEN_2D_Parameters.SetGrowthRate(k_global)
NETGEN_2D_Parameters.SetQuadAllowed(quad_elem)

global_elem_size = Mesh_2D.Segment().LocalLength(length_elem,None,1e-07)

numSegmentsCircle = Mesh_2D.Segment(geom=circle_edge)
nMeshCircle = numSegmentsCircle.NumberOfSegments(nC)
smesh.SetName(numSegmentsCircle.GetSubMesh(), 'subMeshCircle')

Viscous_Layers_walls = NETGEN_2D.ViscousLayers2D(wall_layer,nWall_layer, k_wall,[ 10, 3 ],0)
Viscous_Layers_circle = NETGEN_2D.ViscousLayers2D(circle_layer, nCircle_layer, k_wall,[ 12 ],0)

status = Mesh_2D.AddHypothesis(Viscous_Layers_walls)

isDone = Mesh_2D.Compute()

circle_edge = Mesh_2D.GroupOnGeom(circle_edge,'circle',SMESH.EDGE)
walls_edge = Mesh_2D.GroupOnGeom(walls_edge,'walls',SMESH.EDGE)
inlet_edge = Mesh_2D.GroupOnGeom(inlet_edge,'inlet',SMESH.EDGE)
outlet_edge = Mesh_2D.GroupOnGeom(outlet_edge,'outlet',SMESH.EDGE)
wall_surf = Mesh_2D.GroupOnGeom(diff_obstacle_2d,'empty',SMESH.FACE)

mesh_group = Mesh_2D.GetGroups()
extrud_var = Mesh_2D.ExtrusionSweepObjects([], [], [Mesh_2D], [0, 0, h], 1, 1, [], 0, [], [], 0)

for var in extrud_var:
  if '_extruded' in var.GetName():
    var.SetName(var.GetName().split('_extruded')[0])
  elif '_top' in var.GetName():
    var.SetName(var.GetName().split('_top')[0]+'2')
  else:
    pass

smesh.SetName(Mesh_2D.GetMesh(), 'Mesh_2D')
smesh.SetName(numSegmentsCircle, 'circle_edge')
smesh.SetName(inlet_edge, 'inlet_edge')
smesh.SetName(walls_edge, 'walls_edge')
smesh.SetName(group_IO, 'group_IO')
smesh.SetName(outlet_edge, 'outlet_edge')

export_to_foam(Mesh_2D, mesh_name=None, export_path=parameters['case_path'])
#export_to_elmer(MeshName, dirname=parameters['elmer_export_path'])


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
