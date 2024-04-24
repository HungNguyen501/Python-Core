"""Cleaning invalid datasets on DataHub"""
from typing import List, Generator
import asyncio
import sys

from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph


def search_datasets(graph: DataHubGraph, search_pattern: str) -> Generator[dict, None, None]:
    """Fetch list of datasets that matches searched pattern

    Args:
        search_pattern(str): pattern for searching

    Returns list of datasets
    """
    query = """
    {{
        search(
            input: {{
                type: DATASET,
                query: "urn:li:dataPlatform:hdfs,zalopay.",
                start: {start}, count: {count}
            }}
        )
        {{
            start
            count
            total
            searchResults {{
                entity {{
                    ...on Dataset {{
                        urn
                        name
                        deprecation {{
                            deprecated
                        }}
                        properties {{
                            customProperties {{
                                key
                                value
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}"""
    start = 0
    batch_size = 100
    total = sys.maxsize
    while start < total:
        print(start)
        results = graph.execute_graphql(
            query=query.format(search_pattern=search_pattern, start=start, count=batch_size)
        )["search"]
        total = results["total"]
        start += batch_size
        yield results["searchResults"]


def extract_dataset_info(li_datasets: List[dict]) -> List[dict]:
    """Filter datasets and extract info from them

    Args:
        li_datasets(list): list of input datasets

    Returns list of datasets
    """
    results = []
    dbs = set()
    for dataset in li_datasets:
        entity = dataset["entity"]
        if entity.get("properties"):
            if entity["properties"].get("customProperties"):
                properties = {p["key"]: p["value"]
                              for p in entity["properties"]["customProperties"]}
                try:
                    if properties["database"] == "hdfs_cluster_61":
                        results.append({
                            "urn": entity["urn"],
                            "location": properties["location"],
                            "deprecation": entity["deprecation"],
                            "database": properties["database"],
                        })
                    dbs.add(properties["database"])
                except KeyError as exc:
                    print(f"{exc}: {entity}")
    print(f"list of dbs: {dbs}")
    return results


async def check_hdfs_path_exists(path: str) -> bool:
    """Verify whether the path exists in HDFS

    Args:
        path(str): path for validation
    """
    process = await asyncio.create_subprocess_shell(
        f"hdfs dfs -conf /home/hungnd8/hdfs_configs/zalopaynewcluster/hdfs-site.xml -test -d {path}",
    )
    await process.wait()
    return process.returncode == 0


async def verify_entity(entity: dict, li_invalids: List[str], semaphore_config: asyncio.Semaphore):
    """Detect invalid entity in datasets

    Args:
        entity(dict): eneity in datasets
        li_invalids(List[str]): list of invalid entities
        semaphore_config(asyncio.Semaphore): semaphore configuration to control number of asynchorous processes
    """
    if entity.get("deprecation") and entity["deprecation"]["deprecated"]:
        print(f"deprecated: {entity['urn']}")
        li_invalids.append(entity["urn"])
        return
    hdfs_path = "hdfs://zalopaynewcluster/" + entity["location"]
    async with semaphore_config:
        if await check_hdfs_path_exists(path=hdfs_path) is False:
            print(f"path doesnot exist [{hdfs_path}]: {entity['urn']}")
            li_invalids.append(entity["urn"])


async def get_list_invalid_hdfs_datasets(
    li_datasets: List[dict],
    li_invalids: List[str]
):
    """Get list of invalid dataset for hdfs_source

    Args:
        li_datasets(list): list of input datasets
        li_invalids(list): list of output datasets
    """
    max_number_processes = 50
    semaphore_config = asyncio.Semaphore(value=max_number_processes)
    tasks = [
        verify_entity(entity=entity, li_invalids=li_invalids, semaphore_config=semaphore_config)
        for entity in li_datasets
    ]
    await asyncio.gather(*tasks)


def remove_datasets(graph: DataHubGraph, li_urns: List[dict]):
    """Remove datasets by its urn

    Args:
        li_urns(list): list of urns
    """
    for urn in li_urns:
        graph.delete_entity(urn=urn, hard=False)


def fetch_schema(graph: DataHubGraph, urn: str) -> dict:
    """Fetch schema of dataset from datahub
    Documents: https://datahubproject.io/docs/graphql/objects/#dataset

    Args:
        urn(str): urn of dataset

    Returns:
        schema as a dict
    """
    query = """
    {{
        dataset(urn: "{urn}") {{
            urn
            name
            type
            lastIngested
            platform {{
                name
            }}
            schemaMetadata {{
                fields {{
                    fieldPath
                    nativeDataType
                }}
            }}
            editableSchemaMetadata {{
                editableSchemaFieldInfo {{
                    fieldPath
                    description
                    tags {{
                        tags {{
                            tag {{
                                name
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
    """
    return graph.execute_graphql(query=query.format(urn=urn))


if __name__ == "__main__":
    dh_graph = DataHubGraph(
        config=DatahubClientConfig(
            server="http://10.60.37.10:8079",
        )
    )
    list_datasets = []
    list_invalid_urns = []
    for i in search_datasets(graph=dh_graph, search_pattern="urn:li:dataPlatform:hdfs,zalopay.encrypt"):
        list_datasets.extend(i)
    hdfs_datasets = extract_dataset_info(li_datasets=list_datasets)
    asyncio.run(main=get_list_invalid_hdfs_datasets(
        li_datasets=list_datasets,
        li_invalids=list_invalid_urns,
    ))
    remove_datasets(graph=dh_graph, li_urns=list_invalid_urns)
