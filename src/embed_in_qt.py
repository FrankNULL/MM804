import vtk
import sys
import os
from PyQt5 import QtCore, QtGui
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog
from tumor_ui import Ui_MainWindow
# from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5 import Qt

class TumorViewerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,  parent=None):
        #Parent constructor
        super(TumorViewerApp,self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.setup)
        self.pushButton1.clicked.connect(self.end)
    def setup(self):
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl = Qt.QVBoxLayout()  
        self.vl.addWidget(self.vtkWidget)

        

        #Reader
        reader = vtk.vtkDICOMImageReader()
        reader2 = vtk.vtkDICOMImageReader()
        colors = vtk.vtkNamedColors()

        reader.SetDirectoryName('35623.000000-FLAIRreg-79237')
        reader2.SetDirectoryName('5388.000000-MaskTumor-63335')

    
        # Marching Cubes Algorithm
        contourFilter = vtk.vtkContourFilter()
        contourFilter.SetInputConnection(reader.GetOutputPort())
        contourFilter.GenerateValues(5, 80.0, 100.0)
        outliner = vtk.vtkOutlineFilter()
        outliner.SetInputConnection(reader.GetOutputPort())
        outliner.Update()

        # create mapper 

        mapper1 = vtk.vtkPolyDataMapper()
        mapper1.SetInputConnection(contourFilter.GetOutputPort())
        mapper1.SetScalarVisibility(0)

        # create actor 
        actor = vtk.vtkActor()
        actor.SetMapper(mapper1)
        actor.GetProperty().SetDiffuse(0.8)
        actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
        actor.GetProperty().SetSpecular(0.8)
        actor.GetProperty().SetSpecularPower(120.0)

        mapper2 = vtk.vtkFixedPointVolumeRayCastMapper()
        mapper2.SetInputConnection(reader2.GetOutputPort())
        mapper2.SetBlendModeToMaximumIntensity()

        colorFunc2 = vtk.vtkColorTransferFunction() 
        r = self.slider.value()
        g = self.slider1.value()
        b = self.slider2.value()
        colorFunc2.AddRGBSegment(0.0, 0.0, 0.0, 0.0, 100, r, g, b)
        opacityWindow2 = 400
        opacityLevel2  = 10
        opacityFunc2 = vtk.vtkPiecewiseFunction()
        opacityFunc2.AddSegment(opacityLevel2 - 0.5*opacityWindow2, 0.0,opacityLevel2 + 0.5*opacityWindow2, 1.0 )
        property2 = vtk.vtkVolumeProperty()
        property2.SetIndependentComponents(True)
        property2.SetColor(colorFunc2)
        property2.SetScalarOpacity(opacityFunc2)
        property2.SetInterpolationTypeToLinear()

        # create volumn
        volume2 = vtk.vtkVolume()
        volume2.SetMapper(mapper2)
        volume2.SetProperty(property2)

        # create render 
        self.render = vtk.vtkRenderer()
        self.render.SetBackground(0,0,0)
        #render.AddVolume(volume)
        self.render.AddVolume(volume2)
        self.render.AddActor(actor)

    
        self.vtkWidget.GetRenderWindow().AddRenderer(self.render)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.frame.setLayout(self.vl)
        self.show()
        self.iren.Initialize()
        self.iren.Start()
    
    def end(self):
        for i in range(len(self.frame.children())):
            self.frame.children()[i].deleteLater()


   

    


class TumorViewer(QtWidgets.QWidget):
    def __init__(self):
        super(TumerViewer,self).__init__(parent)
        
        interactor = QVTKRenderWindowInteractor(self)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(interactor)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        # render window
        renWin = vtk.vtkRenderWindow()
        renWin.Initialize()
        renWin.AddRenderer(render)
        render.ResetCamera()
        render.GetActiveCamera().SetViewAngle(30)
        
        #Interactor
        self.iren = interactor
        self.iren.SetRenderWindow(renWin)
    
    def start(self):
        self.iren.Start()

if __name__ == "__main__":

    os.chdir(os.path.dirname(__file__))

    app = QtWidgets.QApplication([])
    main_window = TumorViewerApp()
    main_window.show()
    sys.exit(app.exec_())