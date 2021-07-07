from conans import ConanFile, CMake, tools

class CronCppConan(ConanFile):
    name = "croncpp"
    version = "0.1.0"
    license = "MIT"
    description = "CRON expressions parser"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/mariusbancila/croncpp.git")
        tools.replace_in_file("croncpp/CMakeLists.txt", "add_library(croncpp INTERFACE)",
                              '''add_library(croncpp INTERFACE)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="croncpp")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="include")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
