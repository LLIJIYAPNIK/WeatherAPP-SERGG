from cx_Freeze import setup, Executable

base = "Win32GUI"

build_exe_options = {"packages": ["PyQt5", "requests"],
                     "include_files": ["imgs_256/", "imgs_128/", "icons/", "imgs/", "bg_imgs/",
                                       "cities.db", "current_city.py", "favorite.txt", "main.ui", "icons.py",
                                       "last_city", "main_design.py", "time_dict.py", "weather_dict.py",
                                       "weather_data.py"]}

setup(
    name="serGGey",
    version="0.1",
    description="Hi",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
