py_binary(
    name = "pool_service",
    srcs = ["pool_service.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_pool_service",
    srcs = ["tests/test_pool_service.py"],
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
        "//src/pool_api/services:pool_service",
    ],
)
