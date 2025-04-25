py_library(
    name = "unittest_async",
    srcs = ["main.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_unittest_async",
    srcs = ["tests/test_main.py"],
    main = "tests/test_main.py",
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
        "//src/unittest_async:unittest_async"
    ],
)
