py_binary(
    name = "data_manager",
    srcs = ["data_manager.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_data_manager",
    srcs = ["tests/test_data_manager.py"],
    timeout = "short",
    args = [
        "-vv",
    ],
    tags = [
        "local",
        "requires-network",
        "yourit",
    ],
    deps = [
        "//src/pool_api/repositories:data_manager",
    ],
)
