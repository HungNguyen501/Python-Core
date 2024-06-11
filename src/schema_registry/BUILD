py_library(
    name = "schema_registry",
    srcs = ["schema_registry.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_schema_registry",
    srcs = ["tests/test_schema_registry.py"],
    main = "tests/test_schema_registry.py",
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
        "//src/schema_registry:schema_registry"
    ],
)
