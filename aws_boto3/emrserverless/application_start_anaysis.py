import argparse
import logging

import boto3
import time
from datetime import datetime
import sys
import numpy as np
import botocore
from prettytable import PrettyTable

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info(f"Logger initialized for module: {__name__}")


def current_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


class EMRServerlessOperations(object):
    def __init__(self, client):
        self.client = client
        self.log = logger

    def get_application(self, app_id: str) -> dict:
        self.log.info(f"Getting application: {app_id}")
        payload = {"applicationId": app_id}
        # response = self.client.get_application(**payload)
        response = self.invoke_operation(self.client.get_application, payload)
        # self.log.info(f"Application result: {response}")
        if response is not None and isinstance(response, dict):
            return response.get("application", {})
        return {}

    def get_application_state(self, app_id: str) -> dict:
        application: dict = self.get_application(app_id)
        if application is not None and isinstance(application, dict):
            return application.get("state", None)
        return None

    def start_application(self, app_id: str) -> bool:
        self.log.info(f"Starting application: {app_id}")
        payload = {"applicationId": app_id}
        response = self.invoke_operation(self.client.start_application, payload)
        self.log.info(f"Start Application result: {response}")
        if response is not None and isinstance(response, dict):
            return response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0) == 200
        return False

    def stop_application(self, app_id: str) -> bool:
        self.log.info(f"Stopping application: {app_id}")
        payload = {"applicationId": app_id}
        # response = self.client.get_application(**payload)
        response = self.invoke_operation(self.client.stop_application, payload)
        self.log.info(f"Stop Application result: {response}")
        if response is not None and isinstance(response, dict):
            return response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0) == 200
        return False

    def create_application(self) -> dict:
        pass

    def poll_app_state(
        self, app_id: str, desired_state: str, terminal_states: list
    ) -> bool:
        continue_polling = True
        while continue_polling:
            app_state = self.get_application_state(app_id)
            self.log.info(f"Current state: {app_state}")
            if app_state is None:
                self.log.error(f"Unexpected state: {app_state}.. existing ")
                return False
            if app_state == desired_state:
                self.log.info(f"Reachd desigered state:: {desired_state}")
                return True
            elif app_state in terminal_states:
                self.log.error(
                    f"Reached teminat state: {app_state} in {terminal_states}"
                )
                return False
            time.sleep(1)  # sleep for 1 sec

    def invoke_operation(self, operation, kwargs) -> dict:
        try:
            logger.info(f"Invoke EMR-Serverles API:::")
            return operation(**kwargs)
        except botocore.exceptions.ClientError as ce:
            self.log.error(f"A server side exception occurred: {ce}")
            self.log.error(f"Exception Error::{ce.response['Error']}")
            if ce.response["Error"]["Code"] == "ExpiredTokenException":
                self.log.error("Invalid Credentials found.")

        except botocore.exceptions.BotoCoreError as be:
            self.log.error(f"A client side error: {be.__class__.__name__}: {be}")
            err_meg = str(be).replace("\n", ":: ")
            self.log.error(f"Error message: {err_meg}")
        return None


def display_stats(app_id: str, app_start_latencies: list) -> None:
    np_array = np.array(app_start_latencies)
    latency_table: PrettyTable = PrettyTable()
    latency_table.field_names = ["AppId", "Min", "Max", "Average", "P50", "P90"]
    latency_table.add_row(
        [
            app_id,
            int(np_array.min()),
            int(np_array.max()),
            int(np.average(np_array)),
            int(np.percentile(np_array, 50)),
            int(np.percentile(np_array, 90)),
        ]
    )
    logger.info(f"For the values: {app_start_latencies}, the stats are")
    logger.info(latency_table)


def render_latency_information(app_id: str, start_latency_metadata: dict) -> None:
    app_start_latencies = []
    latency_keys = ["startingTime", "startedTime", "AppStartTime"]
    latency_table: PrettyTable = PrettyTable()
    latency_table.field_names = ["AppId"] + latency_keys

    for i, latency in start_latency_metadata.items():
        if latency.get("AppStartTime", None):
            app_start_latencies.append(latency.get("AppStartTime"))
        row: list = [app_id]
        [row.append(latency.get(key)) for key in latency_keys]
        latency_table.add_row(row)
    logger.info(latency_table)
    # calculate stats.
    display_stats(app_id, app_start_latencies)


def get_app_start_latency(latency):
    start = latency.get("startingTime", None)
    end = latency.get("startedTime", None)
    if start and end:
        return int(end - start)
    return -1


def start_analysis(args_dict: dict) -> None:
    logger.info(f"Argument parsed: {args_dict}")
    application_id = args_dict.get("application_id", None)
    num_runs = args_dict.get("num_runs", None)
    assert application_id is not None
    assert num_runs is not None
    num_runs = int(num_runs)
    logger.info(f"Using application Id: {application_id}")

    # pre-setup
    client = boto3.client(
        "emr-serverless",
        endpoint_url="https://emr-serverless-gamma.us-west-2.amazonaws.com",
    )
    emr_operator = EMRServerlessOperations(client)

    # application start metadata
    start_latency_metadata = {}  # iteration -> {startingTime, startedTime}

    for iterator in range(num_runs):
        latency = {}
        logger.info(f"Iteration: {iterator}")
        app_details = emr_operator.get_application(application_id)
        app_status = app_details.get("state", None)
        logger.info(f"Application current state: {app_status}")
        stop_result = emr_operator.stop_application(application_id)
        logger.info(f"Application stopped: {stop_result}")
        poll_result = emr_operator.poll_app_state(application_id, "STOPPED", [])
        time.sleep(5)  # gap of 5 sec bet stop and start.
        logger.info(f"Application stopped: {poll_result}")
        start_result = emr_operator.start_application(application_id)
        logger.info(f"Application started: {start_result}")
        latency["startingTime"] = time.time() if start_result is True else None
        poll_result = emr_operator.poll_app_state(
            application_id, "STARTED", ["STOPPING", "STOPPED"]
        )
        logger.info(f"Poll Start status: {poll_result}")
        latency["startedTime"] = time.time() if poll_result is True else None
        latency["AppStartTime"] = get_app_start_latency(latency)
        # populate
        logger.info(f"Latency:: {latency}")
        start_latency_metadata[f"{iterator}"] = latency

    logger.info(f"Latency stats::: {start_latency_metadata}")
    render_latency_information(application_id, start_latency_metadata)


if __name__ == "__main__":
    logger.info("Starting Application Start latency analysis..")
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
        "--app-id",
        type=str,
        required=True,
        dest="application_id",
        help="EMR-Serverless Application id",
    )
    argParser.add_argument(
        "--runs",
        type=int,
        required=True,
        dest="num_runs",
        help="Number of time to perform",
    )

    args_parsed = argParser.parse_args()
    args_dict: dict = vars(args_parsed)

    start_analysis(args_dict)
