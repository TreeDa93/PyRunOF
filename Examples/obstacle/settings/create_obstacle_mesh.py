#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.5.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/ivan/science/works/obstacle')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


### GEOMETRY ###

d = 0.01 # diameter of obstacle
betta = 0.25
h = d / betta # z - size of the duct, widht
a = h # y - size of the duct, height
Lu = 12 * d # upstream distance
Ld = 42 * d # downstream distance

### MESH ###
nIO = 100 # точек на входе и выходе
nC = 360  # точек на дуге окружности
nL = 300  # точек по длине канала
Ha = 2160
delta_Ha = a / Ha
delta_Sh  = a / Ha ** 0.5
wall_layer = delta_Sh
circle_layer = 0.01
nWall_layer = 20
nCircle_layer = 96
k_wall = 1.03


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
exportHDmesh = True


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

max_size_elem = 3e-4
length_elem = max_size_elem
min_size_elem = 1e-8
k_global = 0.1
quad_elem = True

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

  
Mesh_2D = smesh.Mesh(diff_obstacle_2d)
NETGEN_2D = Mesh_2D.Triangle(algo=smeshBuilder.NETGEN_2D)
#smesh.SetName(NETGEN_2D.GetAlgorithm(), 'NETGEN 2D')
#Length_From_Edges = NETGEN_2D.LengthFromEdges()

NETGEN_2D_Parameters = NETGEN_2D.Parameters()
NETGEN_2D_Parameters.SetMaxSize(max_size_elem)
NETGEN_2D_Parameters.SetMinSize(min_size_elem)
NETGEN_2D_Parameters.SetFineness(5)
NETGEN_2D_Parameters.SetGrowthRate(k_global)
NETGEN_2D_Parameters.SetQuadAllowed(quad_elem)

global_elem_size = Mesh_2D.Segment().LocalLength(length_elem,None,1e-07)
#Local_Length_1 = circle_edge_3.LocalLength(0.001,None,1e-07)
#smesh.SetName(Length_From_Edges, 'Length From Edges_1')

numSegmentsCircle = Mesh_2D.Segment(geom=circle_edge)
nMeshCircle = numSegmentsCircle.NumberOfSegments(nC)
smesh.SetName(numSegmentsCircle.GetSubMesh(), 'subMeshCircle')

#numSegmentsIO = Mesh_2D.Segment(geom=group_IO)
#nMeshIO = numSegmentsIO.NumberOfSegments(nIO)
#subMesh_IO = numSegmentsIO.GetSubMesh()
#smesh.SetName(numSegmentsIO.GetSubMesh(), 'subMesh_IO')

#numSegmentsLength = Mesh_2D.Segment(geom=walls_edge)
#nMeshLength = numSegmentsLength.NumberOfSegments(nL)
#subMesh_length = numSegmentsLength.GetSubMesh()
#smesh.SetName(numSegmentsLength.GetSubMesh(), 'subMesh_length')

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

from exportMesh import exportMeshToElmer, exportMeshToOF


exportMeshToOF(exportHDmesh, mesh=Mesh_2D, mName='OFmesh')


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
