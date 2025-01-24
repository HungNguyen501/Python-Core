py_binary(
    name = "calculate_statistics",
    srcs = ["main.py"],
    main = "main.py",
    data = [
        "//build:logging.cfg",
        "//src/calculate_statistics:weather_stations.csv",
    ],
    visibility = ["//visibility:public"],
    args = [
        "-f ./src/calculate_statistics/weather_stations.csv",
    ]
)
