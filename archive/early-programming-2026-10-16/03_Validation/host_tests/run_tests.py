from pathlib import Path
import subprocess,tempfile,shutil
root=Path(__file__).resolve().parent
compiler=shutil.which('clang++') or shutil.which('g++')
if not compiler:raise SystemExit('Install a C++17 compiler to run the host tests.')
flags=['-std=c++17','-I',str(root)]
sdk=Path('/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1')
if sdk.exists():flags+=['-isystem',str(sdk)]
with tempfile.TemporaryDirectory(prefix='sd5531_tests_') as tmp:
 for source in sorted(root.glob('test_task*.cpp')):
  binary=Path(tmp)/source.stem
  subprocess.run([compiler,*flags,str(source),'-o',str(binary)],check=True)
  subprocess.run([str(binary)],check=True)
