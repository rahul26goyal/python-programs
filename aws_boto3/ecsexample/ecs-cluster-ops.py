import logging
import sys
from typing import List, Any

import boto3
import botocore.exceptions
import mypy_boto3_ecs.type_defs
from dateutil.tz import tzlocal
from datetime import datetime
from mypy_boto3_ecs.client import ECSClient
from prettytable import PrettyTable
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info(f"Logger initialized for module: {__name__}")


def get_ecs_client() -> ECSClient:
    my_session: boto3.Session = boto3.session.Session(region_name="us-west-2")
    ecs_client: ECSClient = my_session.client("ecs")
    # ecs_client: ECSClient = boto3.client("ecs")
    return ecs_client


class ECSOperation(object):
    def __init__(self, ecs_client: ECSClient):
        self.ecs_client = ecs_client
        self.log = logger

    def list_all_clusters(self):
        self.log.info("Listing all the cluster...")
        try:
            max_result = 100
            all_clusters = []
            next_token = None
            while True:
                payload = {
                    "maxResults": max_result,
                    "nextToken": next_token if next_token is not None else "",
                }
                res: mypy_boto3_ecs.type_defs.ListClustersResponseTypeDef = (
                    ecs_client.list_clusters(**payload)
                )
                # self.log.info(f"Response: {res}")
                cluster_arns = res["clusterArns"]
                [all_clusters.append(c) for c in cluster_arns]
                next_token = res.get("nextToken", None)
                if next_token is None:
                    break
            self.log.info(f"Number of cluster: {len(all_clusters)}")
            self.log.info(f"All cluster::::{all_clusters}")
        except botocore.exceptions.ClientError as ce:
            self.log.error(f"A server side exception occurred: {ce}")
            self.log.error(f"Exception Error::{ce.response['Error']}")
            if ce.response["Error"]["Code"] == "ExpiredTokenException":
                self.log.error("Invalid Credentials found.")

        except botocore.exceptions.BotoCoreError as be:
            self.log.error(f"A client side error: {be.__class__.__name__}: {be}")
            err_meg = str(be).replace("\n", ":: ")
            self.log.error(f"Error message: {err_meg}")
            # if you want to log stack trace..
            # self.log.exception("An Exception occurred:", exc_info=True)


class ECSClusterOperations(ECSOperation):
    def __init__(self, client: ECSClient, cluster_name: str):
        super(ECSClusterOperations, self).__init__(client)
        self.cluster_name_arn = cluster_name
        self.log.info(f"Initialize {self.__class__.__name__}")

    def get_tasks_arn_by_task_definition(self, task_def_name: str) -> List[str]:
        try:
            payload = {
                "cluster": self.cluster_name_arn,
                "family": task_def_name,
                "maxResults": 100,
            }
            response_dict: mypy_boto3_ecs.type_defs.ListTasksResponseTypeDef = (
                self.ecs_client.list_tasks(**payload)
            )
            task_list = response_dict.get("taskArns", [])
            self.log.info(f"Tasks fetched: {task_list}")
            return task_list
        except botocore.exceptions.ClientError as ce:
            self.log.error(f"A server side exception occurred: {ce}")
            self.log.error(f"Exception Error Message::{ce.response['Error']}")
        except botocore.exceptions.BotoCoreError as be:
            err_meg = str(be).replace("\n", ":: ")
            self.log.error(f"Exception Error message: {err_meg}")
        return []

    def describe_tasks(self, task_arns: List[str]) -> dict:
        try:
            payload = {"cluster": self.cluster_name_arn, "tasks": task_arns}
            res_dict: dict = self.ecs_client.describe_tasks(**payload)
            task_to_metadata = {}
            tasks = res_dict.get("tasks", [])

            def convert_to_epoc(_datetime: datetime):
                if _datetime is not None:
                    return _datetime.timestamp()
                return None

            for task in tasks:
                task_obj = {
                    "createdAt": convert_to_epoc(task.get("createdAt", None)),
                    "startedAt": convert_to_epoc(task.get("startedAt", None)),
                    "pullStartedAt": convert_to_epoc(task.get("pullStartedAt", None)),
                    "pullStoppedAt": convert_to_epoc(task.get("pullStoppedAt", None)),
                }
                self.log.info(f"taskobj:: {task_obj}")
                task_obj["pullTime"] = round(
                    task_obj.get("pullStoppedAt", 0) - task_obj.get("pullStartedAt", 0),
                    2,
                )
                task_obj["launchTime"] = round(
                    task_obj["startedAt"] - task_obj["createdAt"], 2
                )
                task_obj["OrchestrationTime"] = round(
                    task_obj["launchTime"] - task_obj["pullTime"], 2
                )
                task_to_metadata[task["taskArn"]] = task_obj

            self.log.info(f"task metadata: {task_to_metadata}")
            return task_to_metadata
        except botocore.exceptions.ClientError as ce:
            self.log.error(f"A server side exception occurred: {ce}")
            self.log.error(f"Exception Error::{ce.response['Error']}")
        except botocore.exceptions.BotoCoreError as be:
            err_meg = str(be).replace("\n", ":: ")
            self.log.error(f"Exception Error message: {err_meg}")
        return {}

    def display_stats(self, container_role: str, task_latencies: dict) -> None:
        latency_table: PrettyTable = PrettyTable()
        latency_table.field_names = [
            "Role",
            "LatencyType",
            "Min",
            "Max",
            "Average",
            "P50",
            "P90",
        ]
        for l_type, latency in task_latencies.items():
            np_array = np.array(latency)
            latency_table.add_row(
                [
                    container_role,
                    l_type,
                    int(np_array.min()),
                    int(np_array.max()),
                    int(np.average(np_array)),
                    int(np.percentile(np_array, 50)),
                    int(np.percentile(np_array, 90)),
                ]
            )
        logger.info(f"For the values: {task_latencies}, the stats are")
        logger.info(latency_table)

    def render_task_latency_information(
        self, task_to_metadata: dict, container_role: str
    ) -> None:
        # sample data

        latency_table: PrettyTable = PrettyTable()
        latency_table.field_names = [
            "Role",
            "taskId",
            "CreateAt",
            "StartedAt",
            "LaunchTime",
            "ImagePullTime",
            "OrchTime",
        ]
        for taskid, metadata in task_to_metadata.items():
            self.log.info(f"{taskid}::{metadata}")
            row = []
            row.append(container_role)
            row.append(taskid.split("/").pop())
            [
                row.append(metadata.get(key, None))
                for key in [
                    "createdAt",
                    "startedAt",
                    "launchTime",
                    "pullTime",
                    "OrchestrationTime",
                ]
            ]
            latency_table.add_row(row)
        self.log.info(latency_table)
        launchTime = [
            metadata.get("launchTime") for taskid, metadata in task_to_metadata.items()
        ]
        pullTime = [
            metadata.get("pullTime") for taskid, metadata in task_to_metadata.items()
        ]
        OrchestrationTime = [
            metadata.get("OrchestrationTime")
            for taskid, metadata in task_to_metadata.items()
        ]
        self.display_stats(
            container_role,
            {
                "launchTime": launchTime,
                "pullTime": pullTime,
                "OrchestrationTime": OrchestrationTime,
            },
        )


if __name__ == "__main__":
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "--cluster",
        type=str,
        dest="cluster_name",
        required=True,
        help="ECS cluster name or arn",
    )
    argParser.add_argument(
        "--task-def",
        type=str,
        dest="task_definition_name",
        required=True,
        help="ECS task definition family name",
    )
    args_ns = argParser.parse_args()
    args: dict = vars(args_ns)  # convert to dict
    ecs_cluster_name = args.get("cluster_name", None)
    task_def_name = args.get("task_definition_name", None)
    container_role = task_def_name.split("-").pop()  # get the last split
    logger.info(f"ECS CLUSTTER NAME: {ecs_cluster_name}")
    logger.info(f"ECS TASK DEF NAME: {task_def_name}")
    # assert ecs_cluster_name is not None, "Cluster name can not be none"
    logger.info(f"Executing ECS examples: {args}")
    ecs_client = get_ecs_client()
    ecs_ops = ECSClusterOperations(ecs_client, ecs_cluster_name)
    # ecs_ops.list_all_clusters()
    # task_to_metadata = {'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/0f1e32c6ec604c1b9b00cf53bb918ae5': {'createdAt': 1690951856.769, 'startedAt': 1690951877.958, 'pullStartedAt': 1690951869.183, 'pullStoppedAt': 1690951876.074, 'pullTime': 6.89, 'launchTime': 21.19, 'OrchestrationTime': 14.3}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/0fa46121c1ba49e482556b23b7d0372a': {'createdAt': 1690951856.769, 'startedAt': 1690951876.709, 'pullStartedAt': 1690951867.905, 'pullStoppedAt': 1690951874.784, 'pullTime': 6.88, 'launchTime': 19.94, 'OrchestrationTime': 13.06}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/24cc90b12fdd40c9a00fe134abe7fbe5': {'createdAt': 1690951858.146, 'startedAt': 1690951878.82, 'pullStartedAt': 1690951870.275, 'pullStoppedAt': 1690951876.997, 'pullTime': 6.72, 'launchTime': 20.67, 'OrchestrationTime': 13.95}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/3075fa5f2c654bc2a20e5c831a2e5f06': {'createdAt': 1690951858.146, 'startedAt': 1690951877.701, 'pullStartedAt': 1690951869.028, 'pullStoppedAt': 1690951875.774, 'pullTime': 6.75, 'launchTime': 19.56, 'OrchestrationTime': 12.81}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/53e9cbcf4d8e4a04a81c501f716a5ff4': {'createdAt': 1690951856.769, 'startedAt': 1690951877.524, 'pullStartedAt': 1690951868.479, 'pullStoppedAt': 1690951875.328, 'pullTime': 6.85, 'launchTime': 20.75, 'OrchestrationTime': 13.9}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/5854d27d627a4749af93862a7e0eae28': {'createdAt': 1690951858.146, 'startedAt': 1690951879.392, 'pullStartedAt': 1690951870.255, 'pullStoppedAt': 1690951877.073, 'pullTime': 6.82, 'launchTime': 21.25, 'OrchestrationTime': 14.43}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/5f7c156f261e46cea5151667320a55f4': {'createdAt': 1690951858.146, 'startedAt': 1690951877.28, 'pullStartedAt': 1690951868.237, 'pullStoppedAt': 1690951874.918, 'pullTime': 6.68, 'launchTime': 19.13, 'OrchestrationTime': 12.45}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/a5be53910e494368b4f1ce0882936e9d': {'createdAt': 1690951858.146, 'startedAt': 1690951878.558, 'pullStartedAt': 1690951869.333, 'pullStoppedAt': 1690951876.381, 'pullTime': 7.05, 'launchTime': 20.41, 'OrchestrationTime': 13.36}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/b0cd1da0692549e587a93a05e2c4ed5d': {'createdAt': 1690951856.769, 'startedAt': 1690951877.586, 'pullStartedAt': 1690951868.548, 'pullStoppedAt': 1690951875.533, 'pullTime': 6.98, 'launchTime': 20.82, 'OrchestrationTime': 13.84}, 'arn:aws:ecs:us-west-2:59932041:task/TOLEDO_ECS_AWS-TOLEDO-APPLICATION-ARTIFACT-56c4ab42-7d28-1159-7dd0-584328d78283/ee17a3964f674537863ee0b1d3f0c5e6': {'createdAt': 1690951856.769, 'startedAt': 1690951877.282, 'pullStartedAt': 1690951868.084, 'pullStoppedAt': 1690951874.868, 'pullTime': 6.78, 'launchTime': 20.51, 'OrchestrationTime': 13.73}}
    task_to_metadata = {}
    tasks = ecs_ops.get_tasks_arn_by_task_definition(task_def_name)
    task_to_metadata = ecs_ops.describe_tasks(tasks)
    ecs_ops.render_task_latency_information(task_to_metadata, container_role)
