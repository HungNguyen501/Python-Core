py_library(
    name = "datahub",
    srcs = ["datahub.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_datahub",
    srcs = ["tests/test_datahub.py"],
    args = [
        "-vv",
    ],
    tags = [
        "local",
        "requires-network",
        "yourit",
    ],
    deps = [
        "//src/datahub:datahub"
    ],
)