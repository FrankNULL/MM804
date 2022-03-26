import vtk
from vtk import *

#Reader
reader = vtk.vtkDICOMImageReader()
reader2 = vtk.vtkDICOMImageReader()
colors = vtk.vtkNamedColors()

#reader.SetDirectoryName('/home/dharanya/Project/BrainTumour/54879843_20060101/54879843/DICOM/Doe^Pierre [54879843]/20060101 000000 [ - CRANE POLYGONE]/Series 003 [CT - Crane Osseux]') 
#reader.SetDirectoryName('Series 002 [CT - Crane SPC]') 
#reader.SetDirectoryName('/home/dharanya/Project/BrainTumour/54879843_20060101/54879843/DICOM/Doe^Pierre [54879843]/20060101 000000 [ - CRANE POLYGONE]/Series 005 [CT - Crane APC]')    
#reader.SetDirectoryName('/home/dharanya/Project/BrainTumour/37916.000000-T2reg-88910')
reader.SetDirectoryName('35623.000000-FLAIRreg-79237')
reader2.SetDirectoryName('5388.000000-MaskTumor-63335')

# Create a mapper.
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Implementing Marching Cubes Algorithm to create the surface using vtkContourFilter object.
contourFilter = vtk.vtkContourFilter()
contourFilter.SetInputConnection(reader.GetOutputPort())
    # Change the range(2nd and 3rd Paramater) based on your
    # requirement. recomended value for 1st parameter is above 1
contourFilter.GenerateValues(5, 80.0, 100.0)
#contourFilter.SetValue(0, iso_value)

outliner = vtk.vtkOutlineFilter()
outliner.SetInputConnection(reader.GetOutputPort())
outliner.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(contourFilter.GetOutputPort())
mapper.SetScalarVisibility(0)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuse(0.8)
actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
actor.GetProperty().SetSpecular(0.8)
actor.GetProperty().SetSpecularPower(120.0)



#Mapper
'''
mapper = vtk.vtkFixedPointVolumeRayCastMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetBlendModeToMaximumIntensity() '''

mapper2 = vtk.vtkFixedPointVolumeRayCastMapper()
mapper2.SetInputConnection(reader2.GetOutputPort())
mapper2.SetBlendModeToMaximumIntensity()
'''
#Property
colorFunc = vtk.vtkColorTransferFunction() 
colorFunc.AddRGBSegment(0.0, 0.0, 0.0, 0.0, 255.0, 0.5, 0.5, 0.5)
opacityWindow = 4000
opacityLevel  = 1000
opacityFunc = vtk.vtkPiecewiseFunction()
opacityFunc.AddSegment(opacityLevel - 0.5*opacityWindow, 0.0,opacityLevel + 0.5*opacityWindow, 1.0 )
property = vtk.vtkVolumeProperty()
property.SetIndependentComponents(True)
property.SetColor(colorFunc)
property.SetScalarOpacity(opacityFunc)
property.SetInterpolationTypeToLinear() '''

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

#Volume
'''volume = vtk.vtkVolume()
volume.SetMapper(mapper)
volume.SetProperty(property) '''

volume2 = vtk.vtkVolume()
volume2.SetMapper(mapper2)
volume2.SetProperty(property2)

#Renderer
render 	= vtk.vtkRenderer()
render.SetBackground(0,0,0)
#render.AddVolume(volume)
render.AddVolume(volume2)
render.AddActor(actor)

# Rendering window
renWin = vtk.vtkRenderWindow()
renWin.Initialize()
renWin.AddRenderer(render)
render.ResetCamera()
render.GetActiveCamera().SetViewAngle(30)
 
#Interactor
iren 	= vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Start()


'''
colorFunc.AddRGBSegment(0.0, 0.0, 0.0, 0.0, 100.0, 100.0, 100.0, 1.0)
opacityWindow = 4000
opacityLevel  = 1000 '''

