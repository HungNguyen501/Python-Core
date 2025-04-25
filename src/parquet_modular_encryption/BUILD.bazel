py_library(
    name = "kms_client",
    srcs = ["kms_client.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "pme_utils",
    srcs = ["pme_utils.py"],
    visibility = ["//visibility:public"],
)


py_test(
    name = "test_pme_utils",
    srcs = ["tests/test_pme_utils.py"],
    main = "tests/test_pme_utils.py",
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
        "//src/parquet_modular_encryption:kms_client",
        "//src/parquet_modular_encryption:pme_utils",
    ],
)

py_test(
    name = "test_kms_client",
    srcs = ["tests/test_kms_client.py"],
    main = "tests/test_kms_client.py",
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
        "//src/parquet_modular_encryption:kms_client"
    ],
)
