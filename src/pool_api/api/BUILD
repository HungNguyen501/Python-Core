py_binary(
    name = "pool_api",
    srcs = ["pool/pool_api.py"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "pool_router",
    srcs = ["pool/router.py"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "application",
    srcs = ["application.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_pool_api",
    srcs = ["pool/tests/test_pool_api.py"],
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
        "//src/pool_api/api:pool_api",
    ],
)

py_test(
    name = "test_pool_router",
    srcs = ["pool/tests/test_router.py"],
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
        "//src/pool_api/api:pool_router",
    ],
)

py_test(
    name = "test_application",
    srcs = ["tests/test_application.py"],
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
        "//src/pool_api/api:application",
    ],
)
