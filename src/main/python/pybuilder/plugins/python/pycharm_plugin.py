#   -*- coding: utf-8 -*-
#
#   This file is part of PyBuilder
#
#   Copyright 2011-2015 PyBuilder Team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import string

from pybuilder.core import task, description

PROJECT_TEMPLATE = string.Template("""<?xml version="1.0" encoding="UTF-8"?>
<!-- This file has been generated by the PyBuilder PyCharm Plugin -->

<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$$MODULE_DIR$$">
      <sourceFolder url="file://$$MODULE_DIR$$/${source_dir}" isTestSource="false" />${unit_tests}${integration_tests}
      ${output_directory}
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
  <component name="PyDocumentationSettings">
    <option name="myDocStringFormat" value="Plain" />
  </component>
  <component name="TestRunnerService">
    <option name="projectConfiguration" value="Unittests" />
    <option name="PROJECT_TEST_RUNNER" value="Unittests" />
  </component>
</module>""")


def _ensure_directory_present(directory):
    if os.path.exists(directory):
        return

    os.makedirs(directory)


@task
@description("Generates PyCharm development files")
def pycharm_generate(project, logger):
    logger.info("Generating PyCharm project files.")

    pycharm_directory = project.expand_path(".idea")
    project_file_name = "{0}.iml".format(project.name)

    _ensure_directory_present(pycharm_directory)
    unit_tests = ""
    integration_tests = ""
    if project.get_property("dir_source_unittest_python"):
        unit_tests = """\n      <sourceFolder url="file://$MODULE_DIR$/""" + project.get_property(
            "dir_source_unittest_python") + """" isTestSource="true" />"""
    if project.get_property("dir_source_integrationtest_python"):
        integration_tests = """\n      <sourceFolder url="file://$MODULE_DIR$/""" + project.get_property(
            "dir_source_integrationtest_python") + """" isTestSource="true" />"""
    output_directory = """<excludeFolder url="file://$MODULE_DIR$/%s" />""" % project.get_property(
            "dir_target")
    project_metadata = PROJECT_TEMPLATE.substitute({
        "source_dir": project.get_property("dir_source_main_python"),
        "unit_tests": unit_tests,
        "integration_tests": integration_tests,
        "output_directory": output_directory
    })
    project_file_path = os.path.join(pycharm_directory, project_file_name)
    with open(project_file_path, "w") as project_file:
        project_file.write(project_metadata)
