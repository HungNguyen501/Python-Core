###############################################################################################
################################ PYTHON RULES LOADING #########################################
###############################################################################################
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "4912ced70dc1a2a8e4b86cec233b192ca053e82bc72d877b98e126156e8f228d",
    strip_prefix = "rules_python-0.32.2",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.32.2/rules_python-0.32.2.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()

# # TO LOAD ANY EXTERNAL PYTHON LIBRARY, LOAD pip_parse rule
# # DEFINE A REQUIREMENTS_LOCK.TXT FILE AND INSTALL THE DEPENCIES PRESENT IN IThon
# load("@rules_python//python:pip.bzl", "pip_parse")
# # Create a central repo that knows about the dependencies needed from
# # requirements_lock.txt.
# pip_parse(
#     name = "python_deps",
#     requirements_lock = "//:requirements_lock.txt",
# )
# # Load the starlark macro which will define your dependencies.
# load("@python_deps//:requirements.bzl", "install_deps")
# # Call it to define repos for your requirements.
# install_deps()