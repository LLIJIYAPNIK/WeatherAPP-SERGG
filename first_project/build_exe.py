from cx_Freeze import setup, Executable

base = "Win32GUI"

build_exe_options = {"packages": ["ip2geotools", "requests"]}

setup(
    name="serGGey",
    version="0.1",
    description="Hi",
    options={"build_exe": build_exe_options},
    executables=[Executable("geolocation.py", base=base)]
)

