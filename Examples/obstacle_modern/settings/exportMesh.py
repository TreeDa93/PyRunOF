u"""
Script for exporting mesh from Salome to Elmer
"""
# ******************************************************************************
#
#    Copyright (C) 2017-, Juris Vencels
#
#    Authors: Juris Vencels
#    Email:   juris.vencels@gmail.com
#    Web:     http://vencels.com
#    Address: University of Latvia
#             Laboratory for mathematical modelling of
#                 environmental and technological processes
#             Zellu Str. 23, Riga, LV-1002, Latvia
#
#    Original Date: 05.05.2017
#
#    This script is based on salomeToOpenFOAM.py written by Nicolas Edh
#    https://github.com/nicolasedh/salomeToOpenFOAM
#
# *****************************************************************************
#
#    This script is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    salomeToElmer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program (in the file LICENSE); if not, write to the
#    Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#    Boston, MA 02110-1301, USA.
#

import sys
import SMESH
from salome.smesh import smeshBuilder
import os, time

def export_mesh_to_foam(key_export, mesh, case_path):
    """
    Main function. Export the selected mesh.

    Will try to find the selected mesh.
    """
    if key_export is True:
        mesh_path = case_path + "/constant/polyMesh"
        __debugPrint__("found selected mesh exporting to " + mesh_path + ".\n", 1)
        exportToFoam(mesh, mesh_path)
        __debugPrint__("finished exporting\n", 1)

def export_mesh_to_elmer(key_export, mesh, export_path):
    """
        Main function. Export the selected mesh.

        Will try to find the selected mesh.
        """
    if key_export is True:

        print("Exporting mesh to " + outdir + "\n")
        exportToElmer(mesh, outdir)


def exportToElmer(mesh, dirname='salomeToElmer'):
    u"""
    Elmer's native mesh consists of 5 files.

    mesh.header - first line (# nodes, # all elements, # edge and boundary elements)
                  second line (# element types)
                  third and all following lines (type, # elements of this type)

    mesh.names - body and boundary names with their IDs taken from Salome mesh groups.
                 The last 'empty' belongs to edge and boundary elements that do not
                 belong to user specified groups.

    mesh.nodes - every line represents one node (node ID, dummy, X, Y, Z)

    mesh.elements - every line represents one volume element (volume element ID,
                    body ID, type, node1, node2, node3, ...)

    mesh.boundary - every line represents one edge or boundary element (edge or
                    boundary element ID, boundary ID, parent volume element 1,
                    parent volume element 2, type, node1, node2, ...)
    """
    tstart = time.time()

    if not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        fileHeader = open(dirname + "/mesh.header", 'w')
        fileNodes = open(dirname + "/mesh.nodes", 'w')
        fileNames = open(dirname + "/mesh.names", 'w')
        fileElements = open(dirname + "/mesh.elements", 'w')
        fileBoundary = open(dirname + "/mesh.boundary", 'w')
    except Exception:
        print("ERROR: Cannot open files for writting")
        return

    meshIs3D = False
    if mesh.NbVolumes() > 0:
        meshIs3D = True

    # mesh.header
    if meshIs3D:
        print("Exporting 3D mesh..\n")
        fileHeader.write("%d %d %d\n" \
                         % (mesh.NbNodes(), mesh.NbVolumes(), mesh.NbEdges() + mesh.NbFaces()))
    else:
        print("Exporting 2D mesh..\n")
        fileHeader.write("%d %d %d\n" \
                         % (mesh.NbNodes(), mesh.NbFaces(), mesh.NbEdges()))

    elems = {str(k): v for k, v in mesh.GetMeshInfo().items() if v}
    fileHeader.write("%d\n" % (len(elems.values()) - 1))

    elemTypeNames = {'202': 'Entity_Edge', '303': 'Entity_Triangle', \
                     '404': 'Entity_Quadrangle', '504': 'Entity_Tetra', \
                     '605': 'Entity_Pyramid', '706': 'Entity_Penta', \
                     '808': 'Entity_Hexa'}

    for nbr, ele in sorted(elemTypeNames.items()):
        if elems.get(ele):
            fileHeader.write("%s %d\n" % (nbr, elems.get(ele)))

    fileHeader.flush()
    fileHeader.close()

    # mesh.nodes
    points = mesh.GetElementsByType(SMESH.NODE)
    for ni in points:
        pos = mesh.GetNodeXYZ(ni)
        fileNodes.write("%d -1 %.12g %.12g %.12g\n" % (ni, pos[0], pos[1], pos[2]))
    fileNodes.flush()
    fileNodes.close()

    # initialize arrays
    invElemType = {v: k for k, v in elemTypeNames.items()}
    invElemIDs = [mesh.NbGroups() + 1 for el in range(mesh.NbElements())]
    elemGrp = list(invElemIDs)

    edgeIDs = mesh.GetElementsByType(SMESH.EDGE)
    faceIDs = mesh.GetElementsByType(SMESH.FACE)
    elemIDs = edgeIDs + faceIDs
    NbBoundaryElems = mesh.NbEdges()

    if meshIs3D:
        volumeIDs = mesh.GetElementsByType(SMESH.VOLUME)
        elemIDs = elemIDs + volumeIDs
        NbBoundaryElems = NbBoundaryElems + mesh.NbFaces()

    if len(elemGrp) != max(elemIDs):
        raise Exception("ERROR: the number of elements does not match!")

    for el in range(mesh.NbElements()):
        invElemIDs[elemIDs[el] - 1] = el + 1

    # mesh.names
    fileNames.write("! ----- names for bodies -----\n")
    groupID = 1

    if meshIs3D:
        bodyType = SMESH.VOLUME
        boundaryType = SMESH.FACE
    else:
        bodyType = SMESH.FACE
        boundaryType = SMESH.EDGE

    for grp in mesh.GetGroups(bodyType):
        fileNames.write("$ %s = %d\n" % (grp.GetName(), groupID))
        for el in grp.GetIDs():
            elemGrp[invElemIDs[el - 1] - 1] = groupID
        groupID = groupID + 1

    fileNames.write("! ----- names for boundaries -----\n")

    for grp in mesh.GetGroups(boundaryType):
        fileNames.write("$ %s = %d\n" % (grp.GetName(), groupID))
        for el in grp.GetIDs():
            if elemGrp[invElemIDs[el - 1] - 1] > groupID:
                elemGrp[invElemIDs[el - 1] - 1] = groupID
        groupID = groupID + 1

    fileNames.write("$ empty = %d\n" % (mesh.NbGroups() + 1))

    fileNames.flush()
    fileNames.close()

    # mesh.elements
    for el in mesh.GetElementsByType(bodyType):
        elemType = mesh.GetElementGeomType(el)
        elemTypeNbr = int(invElemType.get(str(elemType)))
        fileElements.write("%d %d %d" % (invElemIDs[el - 1] - NbBoundaryElems, \
                                         elemGrp[invElemIDs[el - 1] - 1], elemTypeNbr))
        for nid in mesh.GetElemNodes(el):
            fileElements.write(" %d" % (nid))
        fileElements.write("\n")

    fileElements.flush()
    fileElements.close()

    # mesh.boundary
    for el in elemIDs[:NbBoundaryElems]:
        elemType = mesh.GetElementGeomType(el)
        elemTypeNbr = int(invElemType.get(str(elemType)))

        x, y, z = mesh.BaryCenter(el)
        parents = mesh.FindElementsByPoint(x, y, z, bodyType)

        if len(parents) is 2 and elemTypeNbr is not 202:
            fileBoundary.write("%d %d %d %d %d" \
                               % (invElemIDs[el - 1], elemGrp[invElemIDs[el - 1] - 1], \
                                  invElemIDs[parents[0] - 1] - NbBoundaryElems, \
                                  invElemIDs[parents[1] - 1] - NbBoundaryElems, elemTypeNbr))
        else:
            fileBoundary.write("%d %d %d 0 %d" \
                               % (invElemIDs[el - 1], elemGrp[invElemIDs[el - 1] - 1], \
                                  invElemIDs[parents[0] - 1] - NbBoundaryElems, elemTypeNbr))

        for nid in mesh.GetElemNodes(el):
            fileBoundary.write(" %d" % (nid))
        fileBoundary.write("\n")

    fileBoundary.flush()
    fileBoundary.close()

    print("Done exporting!\n")
    print("Total time: %0.f s\n" % (time.time() - tstart))








u"""
Export a Salome Mesh to OpenFOAM.

It handles all types of cells. Use 
salomeToOpenFOAM.exportToFoam(Mesh_1) 
to export. Optionally an output dir can be given as argument.

It's also possible to select a mesh in the object browser and
run the script via file->load script (ctrl-T).

Groups of volumes will be treated as cellZones. If they are 
present they will be put in the file cellZones. In order to convert
to regions use the OpenFOAM tool 
splitMeshRegions - cellZones

No sorting of faces is done so you'll have to run
renumberMesh -overwrite
In order to use the mesh.
"""
# Copyright 2018
# Author Nicolas Edh,
# Nicolas.Edh@gmail.com (user "nsf" at cfd-online.com)
# Contributor(s):
#   Sam Woodhead
#   sam@blueforge.xyz
#
# License
#
#    This script is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    salomeToOpenFOAM  is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with salomeToOpenFOAM.  If not, see <http://www.gnu.org/licenses/>.
#
#    The license is included in the file LICENSE.
#

import sys
import salome
import SMESH
from salome.smesh import smeshBuilder
import os, time

debug = 1  # Print Verbosity (0=silent => 3=chatty)
verify = False  # Verify face order, might take longer time


# Note: to skip renumberMesh just sort owner
# while moving positions also move neighbour,faces, and bcfaces
# will probably have to first sort the internal faces then bc-faces within each bc

class MeshBuffer(object):
    """
    Limits the calls to Salome by buffering the face and key details of volumes to speed up exporting
    """

    def __init__(self, mesh, v):
        i = 0
        faces = list()
        keys = list()
        fnodes = mesh.GetElemFaceNodes(v, i)
        while fnodes:  # While not empty list
            faces.append(fnodes)  # Face list
            keys.append(tuple(sorted(fnodes)))  # Buffer key
            i += 1
            fnodes = mesh.GetElemFaceNodes(v, i)

        self.v = v  # The volume
        self.faces = faces  # The sorted face list
        self.keys = keys
        self.fL = i  # The number of faces

    @staticmethod
    def Key(fnodes):
        """Takes the nodes and compresses them into a hashable key"""
        return tuple(sorted(fnodes))

    @staticmethod
    def ReverseKey(fnodes):
        """Takes the nodes and compresses them into a hashable key reversed for baffles"""
        if (type(fnodes) is tuple):
            return tuple(reversed(fnodes))
        else:
            return tuple(sorted(fnodes, reverse=True))


def exportToFoam(mesh, dirname='polyMesh'):
    """
    Export a mesh to OpenFOAM.

    args:
        +    mesh: The mesh
        + dirname: The mesh directory to write to

    The algorithm works as follows:
    [1] Loop through the boundaries and collect all faces in each group.
        Faces that don't have a group will be added to the group defaultPatches.

    [2] Loop through all cells (volumes) and each face in the cell.
        If the face has been visited before it is added to the neighbour list
        If not, then check it is a boundary face.
            If it is, add the cell to the end of owner.
            If not a boundary face and has not yet been visited add it to the list of internal faces.

    To check if a face has been visited a dictionary is used.
    The key is the sorted list of face nodes converted to a string.
    The value is the face id. Eg: facesSorted[key] = value
    """
    starttime = time.time()
    # try to open files
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        filePoints = open(dirname + "/points", 'w')
        fileFaces = open(dirname + "/faces", 'w')
        fileOwner = open(dirname + "/owner", 'w')
        fileNeighbour = open(dirname + "/neighbour", 'w')
        fileBoundary = open(dirname + "/boundary", 'w')
    except Exception:
        print("could not open files aborting")
        return

    # Get salome properties
    smesh = smeshBuilder.New()

    __debugPrint__('Number of nodes: %d\n' % (mesh.NbNodes()))
    volumes = mesh.GetElementsByType(SMESH.VOLUME)
    __debugPrint__("Number of cells: %d\n" % len(volumes))
    __debugPrint__('Counting number of faces:\n')
    # Filter faces
    filter = smesh.GetFilter(SMESH.EDGE, SMESH.FT_FreeFaces)
    extFaces = set(mesh.GetIdsFromFilter(filter))
    nrBCfaces = len(extFaces)
    nrExtFaces = len(extFaces)
    # nrBCfaces=mesh.NbFaces();#number of bcfaces in Salome

    nrFaces = 0
    buffers = list()
    for v in volumes:
        b = MeshBuffer(mesh, v)
        nrFaces += b.fL
        buffers.append(b)

    # all internal faces will be counted twice, external faces once
    # so:
    nrFaces = int((nrFaces + nrExtFaces) / 2)
    nrIntFaces = nrFaces - nrBCfaces  #
    __debugPrint__('total number of faces: %d, internal: %d, external %d\n' \
                   % (nrFaces, nrIntFaces, nrExtFaces))

    __debugPrint__("Converting mesh to OpenFOAM\n")
    faces = []  # list of internal face nodes ((1 2 3 4 ... ))
    facesSorted = dict()  # each list of nodes is sorted.
    bcFaces = []  # list of bc faces (
    bcFacesSorted = dict()
    owner = []  # owner file, (of face id, volume id)
    neighbour = []  # neighbour file (of face id, volume id) only internal faces

    # Loop over all salome boundary elemets (faces)
    # and store them inte the list bcFaces
    grpStartFace = []  # list of face ids where the BCs starts
    grpNrFaces = []  # list of number faces in each BC
    grpNames = []  # list of the group name.
    ofbcfid = 0  # bc face id in openfoam
    nrExtFacesInGroups = 0
    for gr in mesh.GetGroups():
        if gr.GetType() == SMESH.FACE:
            grpNames.append(gr.GetName())
            __debugPrint__('found group \"%s\" of type %s, %d\n' \
                           % (gr.GetName(), gr.GetType(), len(gr.GetIDs())), 2)
            grIds = gr.GetIDs()
            nr = len(grIds)
            if nr > 0:
                grpStartFace.append(nrIntFaces + ofbcfid)
                grpNrFaces.append(nr)
            # loop over faces in group
            for sfid in grIds:
                fnodes = mesh.GetElemNodes(sfid)
                key = MeshBuffer.Key(fnodes)
                if not key in bcFacesSorted:
                    bcFaces.append(fnodes)
                    bcFacesSorted[key] = ofbcfid
                    ofbcfid += 1
                else:
                    raise Exception( \
                        "Error the face, elemId %d, %s belongs to two " % (sfid, fnodes) + \
                        "or more groups. One is : %s" % (gr.GetName()))

            # if the group is a baffle then the faces should be added twice
            if __isGroupBaffle__(mesh, gr, extFaces, grIds):
                nrBCfaces += nr
                nrFaces += nr
                nrIntFaces -= nr
                # since nrIntFaces is reduced all previously grpStartFaces are
                # out of sync
                grpStartFace = [x - nr for x in grpStartFace]
                grpNrFaces[-1] = nr * 2
                for sfid in gr.GetIDs():
                    fnodes = mesh.GetElemNodes(sfid)
                    key = MeshBuffer.ReverseKey(fnodes)
                    bcFaces.append(fnodes)
                    bcFacesSorted[key] = ofbcfid
                    ofbcfid += 1
            else:
                nrExtFacesInGroups += nr

    __debugPrint__('total number of faces: %d, internal: %d, external %d\n' \
                   % (nrFaces, nrIntFaces, nrExtFaces), 2)
    # Do the defined groups cover all BC-faces?
    if nrExtFacesInGroups < nrExtFaces:
        __debugPrint__("Warning, some elements don't have a group (BC). " + \
                       "Adding to a new group called defaultPatches\n", 1)
        grpStartFace.append(nrIntFaces + ofbcfid)
        grpNrFaces.append(nrExtFaces - nrExtFacesInGroups)
        salomeIDs = []
        for face in extFaces:
            fnodes = mesh.GetElemNodes(face)
            key = MeshBuffer.Key(fnodes)
            try:
                bcFacesSorted[key]
            except KeyError:
                # if not in dict then add to default patches
                bcFaces.append(fnodes)
                bcFacesSorted[key] = ofbcfid
                salomeIDs.append(face)
                ofbcfid += 1
        newGrpName = "defaultPatches"
        nri = 1
        while newGrpName in grpNames:
            newGrpName = "defaultPatches_%d" % nri
            nri += 1
        grpNames.append(newGrpName)
        # function might have different name
        try:
            defGroup = mesh.CreateGroup(SMESH.FACE, newGrpName)
        except AttributeError:
            defGroup = mesh.CreateEmptyGroup(SMESH.FACE, newGrpName)

        defGroup.Add(salomeIDs)
        smesh.SetName(defGroup, newGrpName)
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser(1)

    # initialise the list faces vs owner/neighbour cells
    owner = [-1] * nrFaces
    neighbour = [-1] * nrIntFaces
    __debugPrint__("Finished processing boundary faces\n")
    __debugPrint__('bcFaces: %d\n' % (len(bcFaces)), 2)
    __debugPrint__(str(bcFaces) + "\n", 3)
    __debugPrint__('bcFacesSorted: %d\n' % (len(bcFacesSorted)), 2)
    __debugPrint__(str(bcFacesSorted) + "\n", 3)
    __debugPrint__('owner: %d\n' % (len(owner)), 2)
    __debugPrint__(str(owner) + "\n", 3)
    __debugPrint__('neighbour: %d\n' % (len(neighbour)), 2)
    __debugPrint__(str(neighbour) + "\n", 3)

    offid = 0;
    ofvid = 0;  # volume id in openfoam
    for b in buffers:

        if debug > 2:  # Salome call only if verbose
            nodes = mesh.GetElemNodes(b.v)
            __debugPrint__('volume id: %d, num nodes %d, nodes:%s \n' % (b.v, len(nodes), nodes), 3)

        fi = 0  # Face index
        while fi < b.fL:
            fnodes = b.faces[fi]
            key = b.keys[fi]
            # Check if the node is already in list
            try:
                fidinof = facesSorted[key]
                # if faceSorted didn't throw an exception then the face is
                # already in the dict. Its an internal face and should be added
                # to the neighbour list
                # print "fidinof %d" %fidinof
                neighbour[fidinof] = ofvid
                __debugPrint__('\tan owner already exist for %d, %s, cell %d\n' % (fi, fnodes, ofvid), 3)
            except KeyError:
                # the face is not in the list of internal faces
                # it might a new face or a BCface.
                try:
                    bcind = bcFacesSorted[key]
                    # if no exception was trown then it's a bc face
                    __debugPrint__('\t found bc face: %d, %s, cell %d\n' % (bcind, fnodes, ofvid), 3)
                    # if the face belongs to a baffle then it exits twice in owner
                    # check dont overwrite owner
                    if owner[nrIntFaces + bcind] == -1:
                        owner[nrIntFaces + bcind] = ofvid
                        bcFaces[bcind] = fnodes
                    else:
                        # build functions that looks for baffles in bclist. with bcind
                        key = MeshBuffer.ReverseKey(fnodes)
                        bcind = bcFacesSorted[key]
                        # make sure the faces has the correct orientation
                        bcFaces[bcind] = fnodes
                        owner[nrIntFaces + bcind] = ofvid
                except KeyError:
                    # the face is not in bc list either so it's a new internal face
                    __debugPrint__('\t a new face was found, %d, %s, cell %d\n' % (fi, fnodes, ofvid), 3)
                    if verify:
                        if not __verifyFaceOrder__(mesh, nodes, fnodes):
                            __debugPrint__("\t face has bad order, reversing order\n", 3)
                            fnodes.reverse()
                    faces.append(fnodes)
                    key = b.keys[fi]
                    facesSorted[key] = offid
                    owner[offid] = ofvid
                    offid += 1
                    if (nrFaces > 50 and offid % (nrFaces / 50) == 0):
                        if (offid % ((nrFaces / 50) * 10) == 0):
                            __debugPrint__(':', 1)
                        else:
                            __debugPrint__('.', 1)
            fi += 1

        ofvid += 1
        # end for v in volumes

    nrCells = ofvid
    __debugPrint__("Finished processing volumes.\n")
    __debugPrint__('faces: %d\n' % (len(faces)), 2)
    __debugPrint__(str(faces) + "\n", 3)
    __debugPrint__('facesSorted: %d\n' % (len(facesSorted)), 2)
    __debugPrint__(str(facesSorted) + "\n", 3)
    __debugPrint__('owner: %d\n' % (len(owner)), 2)
    __debugPrint__(str(owner) + "\n", 3)
    __debugPrint__('neighbour: %d\n' % (len(neighbour)), 2)
    __debugPrint__(str(neighbour) + "\n", 3)

    # Convert to "upper triangular order"
    # owner is sorted, for each cell sort faces it's neighbour faces
    # i.e. change
    # owner   neighbour          owner   neighbour
    #     0          15                    0                3
    #     0            3          to       0              15
    #     0           17                   0              17
    #     1            5                    1                5
    # any changes made to neighbour are repeated to faces.
    __debugPrint__("Sorting faces in upper triangular order\n", 1)
    ownedfaces = 1
    for faceId in range(0, nrIntFaces):
        cellId = owner[faceId]
        nextCellId = owner[faceId + 1]  # np since len(owner) > nrIntFaces
        if cellId == nextCellId:
            ownedfaces += 1
            continue

        if ownedfaces > 1:
            sId = faceId - ownedfaces + 1  # start ID
            eId = faceId  # end ID
            inds = list(range(sId, eId + 1))
            inds.sort(key=neighbour.__getitem__)
            neighbour[sId:eId + 1] = map(neighbour.__getitem__, inds)
            faces[sId:eId + 1] = map(faces.__getitem__, inds)

        ownedfaces = 1
    converttime = time.time() - starttime

    # WRITE points to file
    __debugPrint__("Writing the file points\n")
    __writeHeader__(filePoints, "points")
    points = mesh.GetElementsByType(SMESH.NODE)
    nrPoints = len(points)
    filePoints.write("\n%d\n(\n" % (nrPoints))
    for n, ni in enumerate(points):
        pos = mesh.GetNodeXYZ(ni)
        filePoints.write("\t(%16.12g %16.12g %16.12g)\n" % (pos[0], pos[1], pos[2]))
    filePoints.write(")\n")
    filePoints.flush()
    filePoints.close()

    # WRITE faces to file
    __debugPrint__("Writing the file faces\n")
    __writeHeader__(fileFaces, "faces")
    fileFaces.write("\n%d\n(\n" % (nrFaces))
    for node in faces:
        fileFaces.write("\t%d(" % (len(node)))
        for p in node:
            # salome starts to count from one, OpenFOAM from zero
            fileFaces.write("%d " % (p - 1))
        fileFaces.write(")\n")
    # internal nodes are done output bcnodes
    for node in bcFaces:
        fileFaces.write("\t%d(" % (len(node)))
        for p in node:
            # salome starts to count from one, OpenFOAM from zero
            fileFaces.write("%d " % (p - 1))
        fileFaces.write(")\n")
    fileFaces.write(")\n")
    fileFaces.flush()
    fileFaces.close()

    # WRITE owner to file
    __debugPrint__("Writing the file owner\n")
    __writeHeader__(fileOwner, "owner", nrPoints, nrCells, nrFaces, nrIntFaces)
    fileOwner.write("\n%d\n(\n" % (len(owner)))
    for cell in owner:
        fileOwner.write(" %d \n" % (cell))
    fileOwner.write(")\n")
    fileOwner.flush()
    fileOwner.close()

    # WRITE neighbour
    __debugPrint__("Writing the file neighbour\n")
    __writeHeader__(fileNeighbour, "neighbour", nrPoints, nrCells, nrFaces, nrIntFaces)
    fileNeighbour.write("\n%d\n(\n" % (len(neighbour)))
    for cell in neighbour:
        fileNeighbour.write(" %d\n" % (cell))
    fileNeighbour.write(")\n")
    fileNeighbour.flush()
    fileNeighbour.close()

    # WRITE boundary file
    __debugPrint__("Writing the file boundary\n")
    __writeHeader__(fileBoundary, "boundary")
    fileBoundary.write("%d\n(\n" % len(grpStartFace))
    for ind, gname in enumerate(grpNames):
        fileBoundary.write("\t%s\n\t{\n" % gname)
        fileBoundary.write("\ttype\t\t")
        if "wall" in gname.lower():
            fileBoundary.write("wall;\n")
        elif "empty" in gname.lower():
            fileBoundary.write("empty;\n")
        else:
            fileBoundary.write("patch;\n")
        fileBoundary.write("\tnFaces\t\t%d;\n" % grpNrFaces[ind])
        fileBoundary.write("\tstartFace\t%d;\n" % grpStartFace[ind])
        fileBoundary.write("\t}\n")
    fileBoundary.write(")\n")
    fileBoundary.close()

    # WRITE cellZones
    # Count number of cellZones
    nrCellZones = 0;
    cellZonesName = list();
    for grp in mesh.GetGroups():
        if grp.GetType() == SMESH.VOLUME:
            nrCellZones += 1
            cellZonesName.append(grp.GetName())
    if nrCellZones > 0:
        try:
            fileCellZones = open(dirname + "/cellZones", 'w')
        except Exception:
            print("Could not open the file cellZones, other files are ok.")
        __debugPrint__("Writing file cellZones\n")
        # create a dictionary where salomeIDs are keys
        # and OF cell ids are values.
        scToOFc = dict([sa, of] for of, sa in enumerate(volumes))
        __writeHeader__(fileCellZones, "cellZones")
        fileCellZones.write("\n%d(\n" % nrCellZones)
        for grp in mesh.GetGroups():
            if grp.GetType() == SMESH.VOLUME:
                fileCellZones.write(grp.GetName() + "\n{\n")
                fileCellZones.write("\ttype\tcellZone;\n")
                fileCellZones.write("\tcellLabels\tList<label>\n")
                cellSalomeIDs = grp.GetIDs()
                nrGrpCells = len(cellSalomeIDs)
                fileCellZones.write("%d\n(\n" % nrGrpCells)
                for csId in cellSalomeIDs:
                    ofID = scToOFc[csId]
                    fileCellZones.write("%d\n" % ofID)

                fileCellZones.write(");\n}\n")
        fileCellZones.write(")\n")
        fileCellZones.flush()
        fileCellZones.close()

    totaltime = time.time() - starttime
    __debugPrint__("Finished writing to %s/%s \n" % (os.getcwd(), dirname))
    __debugPrint__("Converted mesh in %.0fs\n" % (converttime), 1)
    __debugPrint__("Wrote mesh in %.0fs\n" % (totaltime - converttime), 1)
    __debugPrint__("Total time: %0.fs\n" % totaltime, 1)


def __writeHeader__(file, fileType, nrPoints=0, nrCells=0, nrFaces=0, nrIntFaces=0):
    """Write a header for the files points, faces, owner, neighbour"""

    file.write("/*" + "-" * 68 + "*\\\n")
    file.write("|" + " " * 70 + "|\n")
    file.write("|" + " " * 4 + "File exported from Salome Platform" + \
               " using SalomeToFoamExporter" + " " * 5 + "|\n")
    file.write("|" + " " * 70 + "|\n")
    file.write("\*" + "-" * 68 + "*/\n")

    file.write("FoamFile\n{\n")
    file.write("\tversion\t\t2.0;\n")
    file.write("\tformat\t\tascii;\n")
    file.write("\tclass\t\t")
    if (fileType == "points"):
        file.write("vectorField;\n")
    elif (fileType == "faces"):
        file.write("faceList;\n")
    elif (fileType == "owner" or fileType == "neighbour"):
        file.write("labelList;\n")
        file.write("\tnote\t\t\"nPoints: %d nCells: %d nFaces: %d nInternalFaces: %d\";\n" \
                   % (nrPoints, nrCells, nrFaces, nrIntFaces))
    elif (fileType == "boundary"):
        file.write("polyBoundaryMesh;\n")
    elif (fileType == "cellZones"):
        file.write("regIOobject;\n")
    file.write("\tlocation\t\"constant/polyMesh\";\n")
    file.write("\tobject\t\t" + fileType + ";\n")
    file.write("}\n\n")


def __debugPrint__(msg, level=1):
    """Print only if level >= debug """
    if (debug >= level):
        print(msg),


def __verifyFaceOrder__(mesh, vnodes, fnodes):
    """
    Verify if the face order is correct. I.e. pointing out of the cell

    calc vol center
    calc f center
    calc ftov=fcenter-vcenter
     calc fnormal=first to second cross first to last
    if ftov dot fnormal >0 reverse order

    """
    vc = __cog__(mesh, vnodes)
    fc = __cog__(mesh, fnodes)
    fcTovc = __diff__(vc, fc)
    fn = __calcNormal__(mesh, fnodes)
    if (__dotprod__(fn, fcTovc) > 0.0):
        return False
    else:
        return True


def __cog__(mesh, nodes):
    """
    calculate the center of gravity.
    """
    c = [0.0, 0.0, 0.0]
    for n in nodes:
        pos = mesh.GetNodeXYZ(n)
        c[0] += pos[0]
        c[1] += pos[1]
        c[2] += pos[2]
    c[0] /= len(nodes)
    c[1] /= len(nodes)
    c[2] /= len(nodes)
    return c


def __calcNormal__(mesh, nodes):
    """
    Calculate and return face normal.
    """
    p0 = mesh.GetNodeXYZ(nodes[0])
    p1 = mesh.GetNodeXYZ(nodes[1])
    pn = mesh.GetNodeXYZ(nodes[-1])
    u = __diff__(p1, p0)
    v = __diff__(pn, p0)
    return __crossprod__(u, v)


def __diff__(u, v):
    """
    u - v, in 3D
    """
    res = [0.0] * 3
    res[0] = u[0] - v[0]
    res[1] = u[1] - v[1]
    res[2] = u[2] - v[2]
    return res


def __dotprod__(u, v):
    """
    3D scalar dot product
    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def __crossprod__(u, v):
    """
    3D cross product
    """
    res = [0.0] * 3
    res[0] = u[1] * v[2] - u[2] * v[1]
    res[1] = u[2] * v[0] - u[0] * v[2]
    res[2] = u[0] * v[1] - u[1] * v[0]
    return res


def findSelectedMeshes():
    meshes = list()
    smesh = smeshBuilder.New()
    nrSelected = salome.sg.SelectedCount()  # total number of selected items

    foundMesh = False
    for i in range(nrSelected):
        selected = salome.sg.getSelected(i)
        selobjID = salome.myStudy.FindObjectID(selected)
        selobj = selobjID.GetObject()
        if selobj.__class__ == SMESH._objref_SMESH_Mesh or selobj.__class__ == salome.smesh.smeshBuilder.meshProxy:
            mName = selobjID.GetName().replace(" ", "_")
            foundMesh = True
            mesh = smesh.Mesh(selobj)
            meshes.append(mesh)

    if not foundMesh:
        print("You have to select a mesh object and then run this script.")
        print("or run the export function directly from TUI")
        print(" import SalomeToOpenFOAM")
        print(" SalomeToOpenFOAM.exportToFoam(mesh,path)")
        return list()
    else:
        return meshes


def __isGroupBaffle__(mesh, group, extFaces, grIds):
    for sid in grIds:
        if not sid in extFaces:
            __debugPrint__("group %s is a baffle\n" % group.GetName(), 1)
            return True
    return False






