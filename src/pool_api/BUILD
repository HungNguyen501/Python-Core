py_binary(
    name = "pool_api",
    srcs = ["api/pool_api.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_pool_api",
    srcs = ["api/tests/test_pool_api.py"],
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
        "//src/pool_api:pool_api",
    ],
)
