import logging
import sys
from typing import List

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

logger = logging.getLogger(__name__)
# defualt logger is warning level
logger.setLevel(logging.DEBUG)
# default logger will write to stderr and only warning level..
# need a explict logger.
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info(f"Logger initialized for module: {__name__}")


def list_ddb_tables(dynamodb: DynamoDBServiceResource):
    all_tables = dynamodb.tables
    logger.info(f"all tables: ${all_tables}")


class InstanceTable(object):
    def __init__(self, dynamodb: DynamoDBServiceResource):
        self.dynamodb: DynamoDBServiceResource = dynamodb
        self.tableName: str = "rhgoyal-ChicagoInstanceMetadata"
        self.table = self.dynamodb.Table(self.tableName)
        # getting a chile logger from the module logger which is defined in the beginning
        self.log = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")
        self.log.info(f"Created object for {self.__class__.__name__}")

    def exists(self):
        try:
            table = self.dynamodb.Table(self.tableName)
            res = table.load()
            logger.info(f"{self.tableName} load: {res}")
        except ClientError as ce:
            self.log.error(f"Failed to check the existence of {self.tableName}: {ce}")
            operation = ce.operation_name
            error_response = ce.response.get("Error", {})
            http_response = ce.response.get("ResponseMetadata", {})
            self.log.error(
                f"Error with op: {operation}: status: {http_response.get('HTTPStatusCode', None)}: error:{error_response.get('Code', 'Unknown')}"
            )
        except Exception as ex:
            logger.exception(f"Exception occurred: {ex}")

    def list_tables(self):
        try:
            tables: List[str] = []
            ddb_tables: List[Table] = self.dynamodb.tables.all()
            self.log.info(f"ddb_tables: {ddb_tables}")
            for table in ddb_tables:
                # self.log.info(table)
                tables.append(table.name)
            self.log.info(f"Tables: {tables}")
        except ClientError as ce:
            self.log.error(f"Failed to check the existence of {self.tableName}: {ce}")
            operation = ce.operation_name
            error_response = ce.response.get("Error", {})
            http_response = ce.response.get("ResponseMetadata", {})
            self.log.error(
                f"Error with op: {operation}: status: {http_response.get('HTTPStatusCode', None)}: error:{error_response.get('Code', 'Unknown')}"
            )
        except Exception as ex:
            logger.exception(f"Exception occurred: {ex}")

    def get_instace_details(self, account_id, instance_id):

        try:
            response = self.table.get_item(
                Key={"accountId": account_id, "instanceId": instance_id}
            )
            logger.info(f"Response: {response}")
            item = response.get("Item", None)
            if item is None:
                self.log.error(f"There is not itm for {account_id}: {instance_id}")
            return item
        except ClientError as ce:
            self.log.error(f"Failed to check the existence of {self.tableName}: {ce}")
            operation = ce.operation_name
            error_response = ce.response.get("Error", {})
            http_response = ce.response.get("ResponseMetadata", {})
            self.log.error(
                f"Error with op: {operation}: status: {http_response.get('HTTPStatusCode', None)}: error:{error_response.get('Code', 'Unknown')}"
            )
        except Exception as ex:
            logger.exception(f"Exception occurred: {ex}")

    def update_instance_state(self, account_id, instance_id, new_state):
        try:
            instance = self.get_instace_details(account_id, instance_id)
            current_state = instance.get("instanceState", None)
            self.log.info(f"Current state is {current_state}")
            response = self.table.update_item(
                Key={"accountId": account_id, "instanceId": instance_id},
                UpdateExpression="SET instanceState = :newState",
                ExpressionAttributeValues={":newState": new_state},
                ConditionExpression="instanceState <> :newState",
            )
            self.log.info(f"Update responsE: {response}")
        except ClientError as ce:
            self.log.error(f"Failed to check the existence of {self.tableName}: {ce}")
            operation = ce.operation_name
            error_response = ce.response.get("Error", {})
            http_response = ce.response.get("ResponseMetadata", {})
            self.log.error(
                f"Error with op: {operation}: status: {http_response.get('HTTPStatusCode', None)}: error:{error_response.get('Code', 'Unknown')}"
            )
            self.log.error(f"Error messages{error_response.get('Message', 'Unknown')}")
        except Exception as ex:
            logger.exception(f"Exception occurred: {ex}")

    def fetch_running_instances(self, account_id):
        try:
            instances = self.table.query(
                KeyConditionExpression="accountId = :accid",
                ExpressionAttributeValues={":accid": account_id, ":state": "RUNNING"},
                FilterExpression="instanceState = :state",
            )
            inst_states = {}
            for inst in instances["Items"]:
                inst_states[inst["instanceId"]] = inst["instanceState"]

            self.log.info(f"States: {inst_states}")
            self.log.info(f"instancs: {instances}")
            return instances
        except ClientError as ce:
            self.log.error(f"Failed to check the existence of {self.tableName}: {ce}")
            operation = ce.operation_name
            error_response = ce.response.get("Error", {})
            http_response = ce.response.get("ResponseMetadata", {})
            self.log.error(
                f"Error with op: {operation}: status: {http_response.get('HTTPStatusCode', None)}: error:{error_response.get('Code', 'Unknown')}"
            )
            self.log.error(
                f"Error messages: {error_response.get('Message', 'Unknown')}"
            )
        except Exception as ex:
            logger.exception(f"Exception occurred: {ex}")

    def fetch_ideal_instances(self, account_id):
        try:
            ddb_query = {
                "KeyConditionExpression": "accountId = :accId",
                "FilterExpression": "instanceState = :running and activeJobCount = :count",
                "ExpressionAttributeValues": {
                    ":accId": account_id,
                    ":running": "RUNNING",
                    ":count": 0,
                },
            }
            response = self.table.query(**ddb_query)
            self.log.info(f"Non ideal instances: {response}")
        except ClientError as ce:
            self.log.error(f"Failed to check the existence of {self.tableName}: {ce}")
            operation = ce.operation_name
            error_response = ce.response.get("Error", {})
            http_response = ce.response.get("ResponseMetadata", {})
            self.log.error(
                f"Error with op: {operation}: status: {http_response.get('HTTPStatusCode', None)}: error:{error_response.get('Code', 'Unknown')}"
            )
            self.log.error(
                f"Error messages: {error_response.get('Message', 'Unknown')}"
            )
        except Exception as ex:
            logger.exception(f"Exception occurred: {ex}")


if __name__ == "__main__":
    try:
        logger.info("Hello DDB client")
        dynamodb: DynamoDBServiceResource = boto3.resource("dynamodb")
        # list_ddb_tables(dynamodb)

        instance_ddb = InstanceTable(dynamodb)
        # instance_ddb.exists()
        # instance_ddb.list_tables()
        # instance_ddb.get_instace_details("59932041", "23vkpnprvtvk2hl83z6wyvy00")
        # instance_ddb.get_instace_details("jdgjasgjag", "23vkpnprvtvk2hl83z6wyvy00")
        # instance_ddb.update_instance_state("59932041", "23vkpnprvtvk2hl83z6wyvy00", "STOPPED")
        # instance_ddb.fetch_running_instances("59932041")
        instance_ddb.fetch_ideal_instances("59932041")

    except Exception as ex:
        logger.exception("Error:")
