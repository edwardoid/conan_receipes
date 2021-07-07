from conans import ConanFile, CMake, tools
from os import rename

class MqttCppConan(ConanFile):
    name = "mqtt_cpp"
    version = "10.0.0"
    license = "Boost"
    author = "DevCodeOne"
    url = "https://github.com/redboltz/mqtt_cpp"
    description = "MQTT client/server for C++14 based on Boost.Asio"
    topics = ("mqtt", "broker", "boost")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "use_tls" : [True, False], "use_websocket": [True, False], \
            "utf8_str_check": [True, False], "use_std_variant": [True, False], "use_std_optional" : [True, False], \
            "use_std_string_view": [True, False], "use_std_any" : [True, False], "use_std_shared_ptr_array" : [True, False], \
            "build_tests" : [True, False], "always_send_reason_code" : [True, False], "build_examples" : [True, False]}
    default_options = {"shared": False, "use_tls": True, "use_websocket" : False, "utf8_str_check" : True, \
            "use_std_variant" : True, "use_std_optional" : True, "use_std_string_view" : True, "use_std_any" : True, \
            "use_std_shared_ptr_array" : True, "build_tests" : False, "build_examples" : True, "always_send_reason_code" : True}
    generators = "cmake"
    requires = "boost/1.76.0"
    exports_sources = "conanfile.py"

    no_copy_source = True

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["MQTT_USE_TLS"] = self.options.use_tls
        cmake.definitions["MQTT_USE_WS"] = self.options.use_websocket
        cmake.definitions["MQTT_USE_STR_CHECK"] = self.options.utf8_str_check
        cmake.definitions["MQTT_STD_VARIANT"] = self.options.use_std_variant
        cmake.definitions["MQTT_STD_OPTIONAL"] = self.options.use_std_optional
        cmake.definitions["MQTT_STD_ANY"] = self.options.use_std_any
        cmake.definitions["MQTT_STD_STRING_VIEW"] = self.options.use_std_string_view
        cmake.definitions["MQTT_STD_SHARED_PTR_ARRAY"] = self.options.use_std_shared_ptr_array
        cmake.definitions["MQTT_BUILD_TESTS"] = self.options.build_tests
        cmake.definitions["MQTT_BUILD_EXAMPLES"] = self.options.build_examples
        cmake.definitions["MQTT_ALWAYS_SEND_REASON_CODE"] = self.options.always_send_reason_code
        cmake.definitions["MQTT_USE_STATIC_BOOST"] = True

        cmake.configure(source_folder="sources")
        return cmake

    def configure(self):
        if self.options.use_tls:
            self.requires("openssl/1.1.1k")

    def source(self):
        git = tools.Git(folder="sources")
        git.clone("https://github.com/redboltz/mqtt_cpp", "v10.0.0")   
        tools.replace_in_file("sources/CMakeLists.txt",
                "PROJECT (mqtt_cpp_iface)",
                              '''PROJECT (mqtt_cpp_iface)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')
        #tools.patch(base_path="sources", patch_file="CMakeLists.patches")
        #tools.patch(base_path="sources", patch_file="Source.patches")

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        if self.options.use_tls:
            self.cpp_info.defines.append("MQTT_USE_TLS=1")

        if self.options.use_websocket:
            self.cpp_info.defines.append("MQTT_USE_WS=1")

        if self.options.utf8_str_check:
            self.cpp_info.defines.append("MQTT_USE_STR_CHECK=1")

        if self.options.use_std_variant:
            self.cpp_info.defines.append("MQTT_STD_VARIANT=1")

        if self.options.use_std_optional:
            self.cpp_info.defines.append("MQTT_STD_OPTIONAL=1")

        if self.options.use_std_any:
            self.cpp_info.defines.append("MQTT_STD_ANY=1")

        if self.options.use_std_string_view:
            self.cpp_info.defines.append("MQTT_STD_STRING_VIEW=1")

        if self.options.use_std_shared_ptr_array:
            self.cpp_info.defines.append("MQTT_STD_SHARED_PTR_ARRAY=1")

        if self.options.always_send_reason_code:
            self.cpp_info.defines.append("MQTT_ALWAYS_SEND_REASON_CODE=1")

        # Probably not needed
        if self.options.build_tests:
            self.cpp_info.defines.append("MQTT_BUILD_TESTS=1")

        if self.options.build_examples:
            self.cpp_info.defines.append("MQTT_BUILD_EXAMPLES=1")

