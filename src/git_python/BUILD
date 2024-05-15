py_library(
    name = "git_ci",
    srcs = ["git_ci.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_git_ci",
    srcs = ["tests/test_git_ci.py"],
    size = "small",
    args = [
        "-vv",
    ],
    tags = [
        "local",
        "requires-network",
        "yourit",
    ],
    deps = [
        "//src/git_python:git_ci"
    ],
)
