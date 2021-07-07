import os
from conans import ConanFile, CMake, tools


class LibserialConan(ConanFile):
    name = "libserial"
    version = "latest"
    license = "BSD 3-Clause"
    author = "Eduard Sargsyan edward.sarkisyan@gmail.com"
    url = "https://github.com/edwardoid/libserial_conan"
    description = "libserial is a library to interact with serial ports on Linux"
    topics = ("Linux", "Serial port")
    settings = "compiler", "build_type", "arch"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}
    generators = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}
#    source_folder = "libserial"

    def configure_cmake(self):
        cmake = CMake(self)
        self.options.shared=True
        cmake.definitions["LIBSERIAL_BUILD_DOCS"] = "NO"
        cmake.definitions["LIBSERIAL_ENABLE_TESTING"] = "NO"
        cmake.definitions["LIBSERIAL_BUILD_EXAMPLES"] = "NO"
        cmake.definitions["LIBSERIAL_PYTHON_ENABLE"] = "NO"
        cmake.definitions["INSTALL_SHARED"] = "ON"
        cmake.definitions["INSTALL_STATIC"] = "OFF"
        cmake.configure(source_folder="libserial")
        return cmake

    def source(self):
        self.run("git clone --depth 1 --branch master  https://github.com/crayzeewulf/libserial.git")

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        includedir = os.path.join(self.package_folder, "include")
        self.cpp_info.includedirs = [includedir]

        libdir = os.path.join(self.package_folder, "lib")
        self.cpp_info.libdirs = [libdir]
        self.cpp_info.libs += tools.collect_libs(self, libdir)
        self.user_info.VERSION = self.version
