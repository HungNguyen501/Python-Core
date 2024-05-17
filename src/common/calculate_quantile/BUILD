py_library(
    name = "calculate_quantile",
    srcs = ["calculate_quantile.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_calculate_quantile",
    srcs = ["tests/test_calculate_quantile.py"],
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
        "//src/common/calculate_quantile:calculate_quantile",
        "//src/pool_api:pool_api",
    ],
)
