from cx_Freeze import setup, Executable

exe=Executable(
     script="Mobilicom graph.py",
     base="Win32Gui",
     icon="MB.ico"
     )
#includefiles=["file.ogg","file.png",etc]
includes=[]
excludes=[]
packages=[]
setup(

     version = "0.0",
     description = "No Description",
     author = "Name",
     name = "App name",
     options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':)},
     executables = [exe]
     )
