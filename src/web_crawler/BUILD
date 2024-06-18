py_library(
    name = "crawler_engine",
    srcs = ["crawler_engine.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_crawler_engine",
    srcs = ["tests/test_crawler_engine.py"],
    main = "tests/test_crawler_engine.py",
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
        "//src/web_crawler:crawler_engine"
    ],
)
