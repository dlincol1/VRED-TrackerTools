from PySide2.QtCore import QTimer
from PySide2.QtGui import QVector3D
    
class xrClippingTools:
    # Clipping tools for Tracker devices - see vrClippingModule for more functions
    
    def __init__(self):
        self.timer = QTimer()
        self.invertClipDirection = False
        self.setAxis('6DoF')
        
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
        
        vrLogInfo('xrClippingTools activated.')
    
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
        
    def clip6DoF(self):            
        # Get World Transform of the geometry plane
        matrix = self.clipPlaneGeo.getWorldTransform()
        setClippingPlane(Pnt3f(matrix[3], matrix[7], matrix[11]),
                         Vec3f(matrix[2], matrix[6], matrix[10]), self.invertClipDirection)

    def clipX(self):    
        matrix = self.clipPlaneGeo.getWorldTransform()
        setClippingPlane(Pnt3f(matrix[3], matrix[7], matrix[11]),
                         Vec3f(1, 0, 0), self.invertClipDirection)

    def clipY(self): 
        matrix = self.clipPlaneGeo.getWorldTransform()
        setClippingPlane(Pnt3f(matrix[3], matrix[7], matrix[11]),
                         Vec3f(0, 1, 0), self.invertClipDirection)
                         
    def clipZ(self): 
        matrix = self.clipPlaneGeo.getWorldTransform()
        setClippingPlane(Pnt3f(matrix[3], matrix[7], matrix[11]),
                         Vec3f(0, 0, 1), self.invertClipDirection)
    
    def clipClone(self):
        cloneClippingContour()
                 
    def setAxis(self, axis):
        if (axis == '6DoF'):
            # Set color to Yellow
            setClippingContourVisualization(True, Vec3f(0.5, 0.5, 0), 1)
            self.timer.timeout.connect(self.clip6DoF)
        elif (axis == 'X'):
            # Set color to Red
            setClippingContourVisualization(True, Vec3f(1, 0, 0), 1)
            self.timer.timeout.connect(self.clipX)
        elif (axis == 'Y'):
            # Set color to Green
            setClippingContourVisualization(True, Vec3f(0, 1, 0), 1)
            self.timer.timeout.connect(self.clipY)
        elif (axis == 'Z'):
            # Set color to Blue
            setClippingContourVisualization(True, Vec3f(0, 0, 1), 1)
            self.timer.timeout.connect(self.clipZ)

enableClippingPlane(True)
xrclip = xrClippingTools()
xrclip.clipStart()
