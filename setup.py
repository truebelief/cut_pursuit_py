from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import sys
import subprocess
import platform

# Get version from environment or hardcoded
def get_version():
    # First, check if VERSION_OVERRIDE is set (CI/CD environment)
    env_version = os.environ.get('VERSION_OVERRIDE')
    if env_version:
        print(f"Using version from environment: {env_version}")
        return env_version
    
    # Fall back to hardcoded version
    return '0.1.2'

# Try to import pybind11, with fallback
try:
    import pybind11
except ImportError:
    print("pybind11 not found. Installing...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pybind11'])
    import pybind11

# Compile sources
cpp_sources = [
    'src/_cut_pursuit.cpp',
    'src/cpp/cut_pursuit.cpp',
    'src/cpp/cut_pursuit_d0.cpp',
    'src/cpp/cp_d0_dist.cpp',
    'src/cpp/maxflow.cpp'
]

# Define extension
ext_modules = [
    Extension(
        'cut_pursuit_py._cut_pursuit',
        sources=cpp_sources,
        include_dirs=[
            pybind11.get_include(),
            os.path.abspath('src'),
            os.path.abspath(os.path.join('src', 'cpp'))
        ],
        language='c++',
    ),
]

# Custom build_ext command
class BuildExt(build_ext):
    def build_extension(self, ext):
        # Add C++11 flag
        if sys.platform == 'win32':
            # Windows with MSVC
            ext.extra_compile_args = ['/std:c++14', '/O2']
        else:
            # Unix-like systems
            ext.extra_compile_args = ['-std=c++11', '-O3']
            
            # Check if we're on PyPy
            if platform.python_implementation() == 'PyPy':
                # Explicitly set the linker for PyPy
                self.compiler.linker_exe = ['g++']
                ext.extra_link_args = ['-shared']
            
        # Call parent build_extension with proper error handling
        try:
            build_ext.build_extension(self, ext)
        except TypeError as e:
            if "NoneType' object is not subscriptable" in str(e) and platform.python_implementation() == 'PyPy':
                print(f"Caught PyPy linker error: {e}")
                print("Attempting with explicit linker configuration...")
                # Even more explicit override for PyPy case
                self.compiler.set_executable('linker_exe', 'g++')
                self.compiler.set_executable('linker_so', 'g++ -shared')
                build_ext.build_extension(self, ext)
            else:
                raise

setup(
    name='cut_pursuit_py',
    version=get_version(),
    author='Zhouxin Xi',
    author_email='truebelief2010@gmail.com',
    description='Cut Pursuit Algorithm for Point Cloud Segmentation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/truebelief/artemis_treeiso/cut_pursuit_py',
    packages=['cut_pursuit_py'],
    package_dir={'cut_pursuit_py': 'src'},
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19.0',
        'pybind11>=2.6.0',
    ],
)
