'''
Based on QuckCreate by MADS HAGBARTH DAMSBO

'''


import nuke

#Base Gridwarp Struct.
#Dear Foundry... could setValue() support?
gridWarpBaseStruct = '''
    1 5 5 4 1 0
    {default }
    {
      { {2 _x0 _y0} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x1 _y0} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x2 _y0} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x3 _y0} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x4 _y0} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x0 _y1} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x1 _y1} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x2 _y1} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x3 _y1} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x4 _y1} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x0 _y2} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x1 _y2} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x2 _y2} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x3 _y2} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x4 _y2} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x0 _y3} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x1 _y3} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x2 _y3} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x3 _y3} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x4 _y3} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x0 _y4} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x1 _y4} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x2 _y4} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x3 _y4} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
      { {2 _x4 _y4} { {2 0 _ty0}  {2 0 -_ty0}  {2 _tx0 0}  {2 -_tx0 0} } } 
    }

'''

def CreateOnSelection(_kind):
    #If the viewer is connected to a node we will use input 0 for ref. Else we just use the viewer itself.
    if nuke.activeViewer().node().input(0):
        myNode = nuke.activeViewer().node().input(0)
        if not nuke.selectedNodes(): #Trying to be smart by assuming that you don't want to add a node to nothing.
            myNode.setSelected(1)
    else:
        myNode = nuke.activeViewer().node()

    bboxinfo = nuke.activeViewer().node()['colour_sample_bbox'].value()    #Get the position info from the colour sample bbox
    aspect = float(myNode.width()*myNode.pixelAspect())/float(myNode.height())  #Calcualte the aspect (thanks Tom van Dop for notifying and Jelmen Palsterman for the correction!)
    cornerA = [(bboxinfo[0]*0.5+0.5)*myNode.width(),(((bboxinfo[1]*0.5)+(0.5/aspect))*aspect)*myNode.height()] #Get the button left corner
    cornerB = [(bboxinfo[2]*0.5+0.5)*myNode.width(),(((bboxinfo[3]*0.5)+(0.5/aspect))*aspect)*myNode.height()] #Get the top right corner
    area_WH = [cornerB[0]-cornerA[0],cornerB[1]-cornerA[1]] #Get the width and height of the bbox
    area_Mid = [cornerA[0]+(area_WH[0]/2),cornerA[1]+(area_WH[1]/2)] #Get the center of the bbox

    if _kind == 'Crop':                     #-----Crop Node-----
        newNode = nuke.Node("Crop")
        newNode['box'].setValue([cornerA[0],cornerA[1],cornerB[0],cornerB[1]])

    elif _kind == 'ROI':                    #-----ROI-----
        nuke.activeViewer().node()["roi"].setValue(bboxinfo)

    elif _kind == 'Transform':              #-----Tranform Node-----
        newNode = nuke.Node("Transform")
        newNode['center'].setValue([area_Mid[0],area_Mid[1]])

    elif _kind == 'GridWarp':               #-----GridWarp Node-----
        newNode = nuke.Node("GridWarp3")
        gridwarpLayout = gridWarpBaseStruct
        for x in range(0,5): #Remap placeholder values to x and y coordinates split up to 5 subdevisions
            gridwarpLayout=gridwarpLayout.replace("_x%s"%x,"%.0f" % (cornerA[0]+((area_WH[0]/4)*x)))
            gridwarpLayout=gridwarpLayout.replace("_y%s"%x,"%.0f" % (cornerA[1]+((area_WH[1]/4)*x)))
        gridwarpLayout=gridwarpLayout.replace("_tx0","%.3f" % (area_WH[0]/12)) #Remap tangent's
        gridwarpLayout=gridwarpLayout.replace("_ty0","%.3f" % (area_WH[1]/12)) #Remap tangent's
        newNode['source_grid_col'].fromScript(gridwarpLayout) #Set Source Grid
        newNode['destination_grid_col'].fromScript(gridwarpLayout) #Set Destination Grid

    if _kind == 'Text':                     
        newNode = nuke.Node("Text2")
        newNode['box'].setValue([cornerA[0],cornerA[1],cornerB[0],cornerB[1]])

    elif _kind == 'Radial':                 
        newNode = nuke.Node("Radial")
        newNode['area'].setValue([cornerA[0],cornerA[1],cornerB[0],cornerB[1]])

    elif _kind == 'Keylight':               
        newNode = nuke.Node("OFXuk.co.thefoundry.keylight.keylight_v201")
        ColorR =  myNode.sample(1,area_Mid[0],area_Mid[1],area_WH[0],area_WH[1])
        ColorG =  myNode.sample(2,area_Mid[0],area_Mid[1],area_WH[0],area_WH[1])
        ColorB =  myNode.sample(3,area_Mid[0],area_Mid[1],area_WH[0],area_WH[1])
        newNode['screenColour'].setValue([ColorR,ColorG,ColorB])        

    elif _kind == 'Tracker':       
        #If we allready have a tracker selexted then append tracks to exsisting tracker node.
        if myNode.Class()=="Tracker4":
          newNode = myNode
          nuke.show(newNode)      
        else:  #Creat a new tracker node
          newNode = nuke.Node("Tracker4")
        numColumns = 31
        colTrackX = 2
        colTrackY = 3
        colRelTrack = 12
        trackIdx = int(newNode["tracks"].toScript().split(" ")[3])
        newNode['add_track'].execute()
        newNode.knob("tracks").setValue(area_Mid[0],numColumns*trackIdx + colTrackX)
        newNode.knob("tracks").setValue(area_Mid[1],numColumns*trackIdx + colTrackY)
        newNode.knob("tracks").setValue(-area_WH[0]/2,numColumns*trackIdx + colRelTrack)
        newNode.knob("tracks").setValue(-area_WH[1]/2,numColumns*trackIdx + colRelTrack+1)
        newNode.knob("tracks").setValue(area_WH[0]/2,numColumns*trackIdx + colRelTrack+2)
        newNode.knob("tracks").setValue(area_WH[1]/2,numColumns*trackIdx + colRelTrack+3)

    elif _kind == 'CornerpinFrom':              
        newNode = nuke.Node("CornerPin2D")
        newNode['from1'].setValue([cornerA[0],cornerA[1]])
        newNode['from2'].setValue([cornerB[0],cornerA[1]])
        newNode['from3'].setValue([cornerB[0],cornerB[1]])
        newNode['from4'].setValue([cornerA[0],cornerB[1]])
    elif _kind == 'CornerpinTo':                
        newNode = nuke.Node("CornerPin2D")
        newNode['to1'].setValue([cornerA[0],cornerA[1]])
        newNode['to2'].setValue([cornerB[0],cornerA[1]])
        newNode['to3'].setValue([cornerB[0],cornerB[1]])
        newNode['to4'].setValue([cornerA[0],cornerB[1]])
    elif _kind == 'CornerpinFromTo':            
        newNode = nuke.Node("CornerPin2D")
        newNode['to1'].setValue([cornerA[0],cornerA[1]])
        newNode['to2'].setValue([cornerB[0],cornerA[1]])
        newNode['to3'].setValue([cornerB[0],cornerB[1]])
        newNode['to4'].setValue([cornerA[0],cornerB[1]])
        newNode['from1'].setValue([cornerA[0],cornerA[1]])
        newNode['from2'].setValue([cornerB[0],cornerA[1]])
        newNode['from3'].setValue([cornerB[0],cornerB[1]])
        newNode['from4'].setValue([cornerA[0],cornerB[1]])
    elif _kind == 'Constant':
        newNode = nuke.Node("Constant", inpanel=False)
        ColorR =  myNode.sample(1,area_Mid[0],area_Mid[1],area_WH[0],area_WH[1])
        ColorG =  myNode.sample(2,area_Mid[0],area_Mid[1],area_WH[0],area_WH[1])
        ColorB =  myNode.sample(3,area_Mid[0],area_Mid[1],area_WH[0],area_WH[1])
        newNode['color'].setValue([ColorR,ColorG,ColorB,1])
