from subprocess import PIPE, Popen

_installed_packages = set()

def install_pip(pipfile):
    if pipfile in _installed_packages:
        return None
    _installed_packages.add(pipfile)
    print(f"installing {pipfile}")
    pip_cmd = ["pip", "install", f"{pipfile}"]
    process = Popen(pip_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout
