class trackerTools(vrAEBase):
    ''' VR Tools for the Vive Tracker '''
    
    def __init__(self):
        vrAEBase.__init__(self)
        self.addLoop()

        # Get the first tracker device
        self.tracker = vrDeviceService.getVRDevice("tracker-1")

        # Create a Transform3D node with a geometry plane as child
        self.trackerTransform = vrNodeService.findNode("trackerTransform")
        
        if not self.trackerTransform.isValid():
            self.trackerTransform = createNode("Transform3D", "trackerTransform", False)
            
            # Create a plane for Clipping position to follow and enable Z axis adjustments
            self.clipPlane = createPlane(25.0, 25.0, 1, 1, 1.0, 0.0, 0.0)
            self.clipPlane.setName('clipPlane')
            self.trackerTransform.addChild(self.clipPlane)
        else:
            self.clipPlane = findNode('clipPlane')
        
        # Constrain Transform3D node to the tracker
        self.trackerConstraint = vrConstraintService.createParentConstraint(
            [self.tracker.getNode()], self.trackerTransform, False)
        
        self.setActive(True)
        vrLogInfo('trackerTools activated')
        
    def __del__(self):
        vrLogInfo('Destructor called, deleting constraint.')
        vrConstraintService.deleteConstraint(self.trackerConstraint)
        
    def updateClippingPosition(self):            
        # Get World Transform of the geometry plane
        matrix = self.clipPlane.getWorldTransform()
            
        # Note, change Vec3f parameters to 1,0,0 for X-axis clipping
        setClippingPlane(Pnt3f(matrix[3], matrix[7], matrix[11]),
                         Vec3f(matrix[2], matrix[6], matrix[10]), invertClipDirection)
    
    def recEvent(self, state):
        vrAEBase.recEvent(self, state)
         
    def loop(self):
        if self.isActive():
            self.updateClippingPosition()

enableClippingPlane(True)
invertClipDirection = True
tracker_tools = trackerTools()