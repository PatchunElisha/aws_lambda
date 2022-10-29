import boto3

region = "ap-northeast-1"


def lambda_handler(event, context):
    # ec2
    ec2_client = boto3.client("ec2", region)
    response = ec2_client.describe_instances()

    ec2_instance_list = {
        "InstanceId": [],
        "Status": [],
    }

    for response in response["Reservations"]:
        ec2_instance_list["InstanceId"].append(response["Instances"][0]["InstanceId"])
        ec2_instance_list["Status"].append(response["Instances"][0]["State"]["Name"])

    if len(ec2_instance_list["InstanceId"]) != 0:
        ec2_id_list = []
        if action == "Start":
            for count, status in enumerate(ec2_instance_list["Status"]):
                if status == "stopped":
                    ec2_id_list.append(ec2_instance_list["InstanceId"][count])

            if len(ec2_id_list) != 0:
                ec2_client.start_instances(InstanceIds=ec2_id_list)
                print("started your instance: " + str(ec2_id_list))
        elif action == "Stop":
            for count, status in enumerate(ec2_instance_list["Status"]):
                if status == "running":
                    ec2_id_list.append(ec2_instance_list["InstanceId"][count])

            if len(ec2_id_list) != 0:
                ec2_client.stop_instances(InstanceIds=ec2_id_list)
                print("stopped your instance: " + str(ec2_id_list))
        else:
            print("Lamdba function could not be executed.")

    # rds
    action = "Start"
    rds_client = boto3.client("rds", region)
    response = rds_client.describe_db_instances()

    rds_instance_list = {
        "DBInstanceIdentifier": [],
        "DBInstanceStatus": [],
    }

    for response in response["DBInstances"]:
        rds_instance_list["DBInstanceIdentifier"].append(
            response["DBInstanceIdentifier"]
        )
        rds_instance_list["DBInstanceStatus"].append(response["DBInstanceStatus"])

    if len(rds_instance_list["DBInstanceIdentifier"]) != 0:
        rds_id_list = []
        if action == "Start":
            for count, status in enumerate(rds_instance_list["DBInstanceStatus"]):
                if status == "stopped":
                    rds_id_list.append(rds_instance_list["DBInstanceIdentifier"][count])

            if len(rds_id_list) != 0:
                for rds_id in rds_id_list:
                    rds_client.start_db_instance(DBInstanceIdentifier=rds_id)
                print("started your rds: " + str(rds_id))
        elif action == "Stop":
            for count, status in enumerate(rds_instance_list["DBInstanceStatus"]):
                if status == "available":
                    rds_id_list.append(rds_instance_list["DBInstanceIdentifier"][count])

            if len(rds_id_list) != 0:
                for rds_id in rds_id_list:
                    rds_client.stop_db_instance(DBInstanceIdentifier=rds_id)
                print("stopped your rds: " + str(rds_id_list))
        else:
            print("Lamdba function could not be executed.")
