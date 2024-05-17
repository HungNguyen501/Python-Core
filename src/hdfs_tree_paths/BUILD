py_library(
    name = "hdfs_tree_paths",
    srcs = ["hdfs_tree_paths.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "test_hdfs_tree_paths",
    srcs = ["tests/test_hdfs_tree_paths.py"],
    timeout = "short",
    args = [
        "-vv",
    ],
    deps = [
        "//src/hdfs_tree_paths:hdfs_tree_paths",
    ],
)
