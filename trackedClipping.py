from PySide2.QtCore import QTimer
    
class xrClippingTools:
    # Clipping tools for Tracker devices, see vrClippingModule for more functions
    
    def __init__(self):
        self.timer = QTimer()
        self.clip_mode = '6DoF'
        self.invertClipDirection = False
        self.timer.timeout.connect(self.update_clip)
        
        # Get the first tracker device
        self.tracker = vrDeviceService.getVRDevice("tracker-1")

        # Create a Transform3D node with a plane as child
        self.trackerTransform = vrNodeService.findNode("trackerTransform")
        
        if not self.trackerTransform.isValid():
            self.trackerTransform = createNode("Transform3D", "trackerTransform", False)
            
            # Create a plane for Clipping position to follow and enable Z axis adjustments
            self.clipPlaneGeo = createPlane(25.0, 25.0, 1, 1, 1.0, 0.0, 0.0)
            self.clipPlaneGeo.setName('clipPlane')
            self.trackerTransform.addChild(self.clipPlaneGeo)
        else:
            self.clipPlaneGeo = findNode('clipPlane')
        
        # Constrain Transform3D node to the tracker
        self.trackerConstraint = vrConstraintService.createParentConstraint(
            [self.tracker.getNode()], self.trackerTransform, False)
        
        annotations = vrAnnotationService.getAnnotations()
        
        if not annotations:
            # List is empty
            self.annotation = vrAnnotationService.createAnnotation("clipping_coordinates")
        else:
            self.annotation = vrAnnotationService.findAnnotation("clipping_coordinates")
        if not self.annotation:
            self.annotation = vrAnnotationService.createAnnotation("clipping_coordinates")
    
        vrLogInfo('xrClippingTools activated.')
        
    def getClippingCoordinates(self):
        clip_coords = vrClippingModule.getClippingPlanePosition()
        vrLogInfo(clip_coords)
        return clip_coords
    
    def __del__(self):
        vrLogInfo('Destructor called, deleting constraint.')
        vrConstraintService.deleteConstraint(self.trackerConstraint)
    
    def clipFlip(self):
        clip_direction = getClippingPlaneInvertDirection()
        
        if (clip_direction):
            self.invertClipDirection = False
        else:
            self.invertClipDirection = True

    def clipStart(self):
        if self.timer.isActive():
            return
        self.timer.start()

    def clipStop(self):
        self.timer.stop()
        vrLogInfo('Clip update stopped.')
    
    def update_clip(self):
        matrix = self.clipPlaneGeo.getWorldTransform()
        matrix_xyz = Pnt3f(matrix[3], matrix[7], matrix[11])
        
        x_coord = str(round(matrix[3], 1))
        y_coord = str(round(matrix[7], 1))
        z_coord = str(round(matrix[11], 1))
        
        self.annotation.setPosition(QVector3D(matrix[3], matrix[7], matrix[11]))

        if self.clip_mode == 'X':
            clip_normal = Vec3f(1, 0, 0)
            self.annotation.setText('X: ' + x_coord)
        elif self.clip_mode == 'Y':
            clip_normal = Vec3f(0, 1, 0)
            self.annotation.setText('Y: ' + y_coord)
        elif self.clip_mode == 'Z':
            clip_normal = Vec3f(0, 0, 1)
            self.annotation.setText('Z: ' + z_coord)
        else:
            clip_normal = Vec3f(matrix[2], matrix[6], matrix[10])
            self.annotation.setText('X: ' + x_coord + '\n' + 'Y: ' + y_coord + '\n' + 'Z: ' + z_coord)

        setClippingPlane(matrix_xyz, clip_normal, self.invertClipDirection)
                 
    def setAxis(self, axis):
        self.clip_mode = axis
        
        if (axis == 'X'):
            setClippingContourVisualization(True, Vec3f(1, 0, 0), 1) # Set color to Red
        elif (axis == 'Y'):
            setClippingContourVisualization(True, Vec3f(0, 1, 0), 1) # Set color to Green
        elif (axis == 'Z'):
            setClippingContourVisualization(True, Vec3f(0, 0, 1), 1) # Set color to Blue
        else:
            setClippingContourVisualization(True, Vec3f(0.5, 0.5, 0), 1) # Set color to Yellow

enableClippingPlane(True)
xrclip = xrClippingTools()
xrclip.clipStart()
