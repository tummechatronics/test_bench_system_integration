#
# Copyright (c) Meysens GmbH 2024. All rights reserved.
#
cmake_minimum_required(VERSION 3.16.0)

project(tpu-tester VERSION 1.0.0)

set(CPACK_PACKAGE_VENDOR "Meysens GmbH")
set(CPACK_PACKAGE_CONTACT "info@toposens.com")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "toposens")
set(CPACK_DEBIAN_PACKAGE_HOMEPAGE "www.toposens.com")

set(CPACK_PACKAGE_INSTALL_DIRECTORY ${CPACK_PACKAGE_NAME})
set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")

set(CPACK_PACKAGE_VERSION_MAJOR ${TOPO_LIB_VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR ${TOPO_LIB_VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH ${TOPO_LIB_VERSION_PATCH})

set(CPACK_VERBATIM_VARIABLES YES)
set(CPACK_DEB_COMPONENT_INSTALL YES)
set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
set(CPACK_DEBIAN_ENABLE_COMPONENT_DEPENDS ON)
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "amd64")

set(CPACK_DEBIAN_PACKAGE_NAME "tpu-tester")
set(CPACK_DEBIAN_FILE_NAME "${CPACK_DEBIAN_PACKAGE_NAME}.deb")
set(CPACK_DEBIAN_DESCRIPTION "TPU tester")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "python3-tk, python3-paramiko, python3-serial")

install(DIRECTORY tpu_tester
    DESTINATION lib/python3/dist-packages
    COMPONENT tpu-tester)

install(PROGRAMS tpu_tester.py
    DESTINATION bin/
    COMPONENT tpu-tester)

install(FILES ${CMAKE_SOURCE_DIR}/config/tpu_tester.desktop
    DESTINATION share/applications
    COMPONENT tpu-tester)

# Install custom icon
install(FILES ${CMAKE_SOURCE_DIR}/config/icons/Topo.png
    DESTINATION share/icons/hicolor/48x48/apps
    COMPONENT tpu-tester)

include(CPack)
