from conans import ConanFile, CMake, tools
from conans import tools


class TgbotConan(ConanFile):
    name = "tgbot"
    version = "latest"

    home = "http://reo7sp.github.io/tgbot-cpp"
    license = "MIT License"
    description = "C++ library for Telegram bot API"

    url = "https://github.com/jgsogo/conan-tgbot"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "use_curl" : [True, False]}
    default_options = {"shared": False, "use_curl" : True}
    generators = ["cmake", "cmake_find_package"]

    @property
    def _source_subfolder(self):
        return "tgbot-cpp"

    def requirements(self):
        self.requires("boost/1.76.0")
        self.requires("openssl/1.1.1k")
        if bool(self.options.use_curl):
            self.requires("libcurl/7.77.0")

    def source(self):
        self.run("git clone https://github.com/edwardoid/tgbot-cpp.git {}".format(self._source_subfolder))
        self.run("cd {}".format(self._source_subfolder, self.version))

        tools.replace_in_file("{}/CMakeLists.txt".format(self._source_subfolder),
                              "project(TgBot)",
                              '''project(TgBot)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_SHARED_LIBS'] = "ON" if bool(self.options.shared) else "OFF"
        cmake.definitions['USE_CURL'] = "ON" if bool(self.options.use_curl) else "OFF"
        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["TgBot"]
