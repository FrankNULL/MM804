import os
import vtk
class TumerViewer:
    def __init__(self):
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
        colorFunc2.AddRGBSegment(0.0, 0.0, 0.0, 0.0, 100.0, 100.0, 100.0, 1.0)
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
        render 	= vtk.vtkRenderer()
        render.SetBackground(0,0,0)
        #render.AddVolume(volume)
        render.AddVolume(volume2)
        render.AddActor(actor)

        # render window
        renWin = vtk.vtkRenderWindow()
        renWin.Initialize()
        renWin.AddRenderer(render)
        render.ResetCamera()
        render.GetActiveCamera().SetViewAngle(30)
        
        #Interactor
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetRenderWindow(renWin)
    
    def start(self):
        self.iren.Start()

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    glyph_viewer = TumerViewer()
    glyph_viewer.start()
    print(glyph_viewer.b0)    


        


