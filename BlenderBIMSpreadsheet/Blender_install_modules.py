import sys
import subprocess

py_exec = str(sys.executable)

# ensure pip is installed
subprocess.call([py_exec, "-m", "ensurepip", "--user" ])

# update pip (not mandatory but highly recommended)
#subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip" ])

# install packages
#subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "openpyxl"])
#subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "pandas"])
#subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "xlsxwriter"])
#subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "pyexcel-ods3"])
#subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "uno"])
#subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "odfpy"])
subprocess.call([py_exec,"-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "unotools"])