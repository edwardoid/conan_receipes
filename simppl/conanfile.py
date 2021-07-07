from conans import ConanFile, tools, CMake
from conans.util import files

class SimpplConan(ConanFile):
    name = "simppl"
    version = "0.3.0"
    settings = "os", "arch", "compiler", "build_type"
    options = {"have_introspection": [True, False]}
    default_options = "have_introspection=True"
    description = "D-Bus is a simple system for interprocess communication and coordination."
    generators = ["cmake_find_package","cmake"]
    requires = ["dbus/1.12.20"]
    def source(self):
        git = tools.Git(folder="simppl")
        git.clone("https://github.com/edwardoid/simppl.git", "master")

    def build(self):
      cmake = CMake(self, parallel=True)
      
      tools.replace_in_file("simppl/CMakeLists.txt", "project(simppl VERSION 0.3.0)", "project(simppl VERSION 0.3.0)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()")
      tools.replace_in_file("simppl/CMakeLists.txt", "install(EXPORT ${PROJECT_NAME}Config DESTINATION /usr/share/simppl/cmake)", "")
      tools.replace_in_file("simppl/CMakeLists.txt", "export(TARGETS ${PROJECT_NAME} FILE simpplConfig.cmake)", "")
      cmake.definitions["SIMPPL_HAVE_INTROSPECTION"] = self.options.have_introspection
      cmake.definitions["SIMPPL_BUILD_EXAMPLES"] = False
      cmake.definitions["SIMPPL_BUILD_TESTS"] = False
      cmake.configure(source_folder="simppl")
      cmake.build()

    def package(self):
      # Libraries
      cmake = CMake(self, parallel=True)
      cmake.install()

    def package_info(self):
        self.cpp_info.defines = []
        if self.options.have_introspection:
            self.cpp_info.defines = ["SIMPPL_HAVE_INTROSPECTION=1"]
        else:
            self.cpp_info.defines = ["SIMPPL_HAVE_INTROSPECTION=0"]
        self.cpp_info.libs = [ "libsimppl.so" ]
        self.cpp_info.includedirs = ['include']  # Ordered list of include paths
        self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
