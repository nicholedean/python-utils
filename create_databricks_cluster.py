"""Script to create databricks cluster given databricks url, username, password
   and cluster details payload (json)

   Example:
   python create_databricks_cluster.py
    --url https://<YOURACCOUNT>.cloud.databricks.com/api/2.0/clusters/create
    --username <USERNAME>
    --password <PASSWORD>
    --payload-path myClusterConfig.json

    Sample payload.json look like below:
    {
        "cluster_name": "mycluster-python3",
        "num_workers": 1,
        "spark_version": "3.3.x-scala2.11",
        "node_type_id": "r3.xlarge",
        "autotermination_minutes": 60,
        "custom_tags": {"stream": "incubation"},
        "aws_attributes": {"instance_profile_arn": "arn:aws:iam::<YOURAWSACCOUNT>:instance-profile\/databricks-s3", "spot_bid_price_percent": "75"},
        "spark_env_vars": {
            "PYSPARK_PYTHON": "\/databricks\/python3\/bin\/python3"
        }
    }
"""
import json
import requests
import click

from click import command, option


@command()
@option('--url', required=True, type=str,
        help="Databricks API URL (prefix with your account identifier)")
@option('--username', required=True, type=str,
        help="Login username. e.g. abc@gmail.com")
@option('--password', required=True, type=str,
        help="Login password")
@option('--json-path', required=True, type=str,
        help="Path to your json payload file")
def main(url, username, password, json_path):
    """Create databricks cluster"""
    with open(json_path, 'r') as myfile:
        parsed_json = json.load(myfile)

    response = requests.post(
        url,
        auth=(username, password),
        json=parsed_json)

    if response.status_code == 200:
        click.echo(response.json()['cluster_id'])
    else:
        click.echo("Error launching cluster: %s: %s" %
                   (response.json()["error_code"], response.json()["message"]))


if __name__ == '__main__':
    main()
