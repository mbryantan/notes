# Airflow 101

https://academy.astronomer.io/path/airflow-101

## Airflow: Local Development Environment

- TODO: Astro setup

- Install providers in your astro instance using requirements.txt
- Upgrade yung astro runtime by editing image version in Dockerfile
- By default, astro docker image is non-base, if you want base version, append to image name with `-base`

## Airflow

### Core Components
- Web server
- Scheduler, in prod should have minimum 2
    - Executor - doesn't execute tasks, defines how to execute your tasks on which system (Kubernetes, Celery, etc.)
- Metastore
- Triggerer - deferred tasks

Additional components:
- Queue
- Worker

### Core Concepts
- DAG
- Operators
    - Action Operators
    - Transfer Operators (move from one place to another)
    - Sensor Operators
- Task Instance
- Workflow

### Summary

1. We have learnt that Airflow is an open-source tool that allows users to author, schedule, and monitor workflows in data pipelines.
1. It is coded in Python and is scalable with a user-friendly interface.
1. We explored the several core components, including the web server, scheduler, meta database, triggerer, executor, queue, and worker.
1. We also learnt about the Directed Acyclic Graph (DAG), which is the most crucial concept, and it represents a data pipeline with nodes as tasks and directed edges as dependencies.
1. Moreover, the Operators are objects that encapsulate tasks, and there are three types of operators: action, transfer, and sensor operators. Providers are packages that contain operators for interacting with specific tools.
1. Airflow works by triggering data pipelines through the scheduler, which creates a DAGRun object and a task instance object for the first task. The task instance is then pushed into a queue and executed by the executor.
1. To create a DAG in Airflow, create a file in the "dags/" folder, instantiate the DAG object with parameters such as the unique DAG ID, start date, scheduling interval, and catchup parameter. Once these parameters are defined, tasks can be implemented within the DAG.
1. To create a task, look up the appropriate operator in the registry.astronomer.io and define the task ID and parameters needed for the operator.
1. Airflow is useful for scheduling batch jobs, training machine learning models, and building ETL or ELT pipelines. It saves time by better scheduling and monitoring data pipelines. However, it is not a data streaming solution or a data processing framework, but an orchestrator for batch processing jobs.
1. We also learnt how to define dependencies in Airflow is simple using the right and left bitshift operators, which can be seen in the Airflow UI. Dependencies can be defined between tasks, such as "start >> end" meaning "end" is executed after "start".

## Airflow: Xcoms 101

### Quiz

Q: Select the 4 factors that define the uniqueness of an XCOM
A: key, dag_id, task_id, logical_date

Q: Is it possible to push an XCOM without explicitly specifying a key?
A: Yes

Q: An XCOM is pushed into..
A: The database

Q: With Postgres, can you share 2Gb of data between 2 tasks with an XCOM?
A: No (max 1GB)

Q: How the Scheduler knows which XCOM to choose for a given DAGRun when multiple XCOMs have the same key, dag_id, and task_id?
A: It selects the XCOM based on the logical date


## Airflow: Sensors

The purpose of a Sensor is to wait for an event.

That can be useful for many different use cases, such as:

-Processing files from an S3 bucket as they arrive while waiting for them.
-Running different tasks at different times but within the same DAG.
-Triggering a data pipeline when another one completes.
-Ensuring an API is available to make requests.
-Transforming data as soon as data are present in a SQL table.

default poke interval: 60 seconds
default timeout: 7 days

Q: You can't find the connection type Amazon Web Services. What should you do?
A: Install the apache-airflow-providers-amazon

Q: If the file never arrives in the S3 bucket. When will the S3KeySensor time out?
A: In 7 days

Q: Does the Sensor instantly detect the file when it arrives in the bucket?
A: No, it depends on the poke_interval

### Custom Sensor Operator Example

```python
from airflow.decorators import dag, task
from datetime import datetime
import requests

from airflow.sensors.base import PokeReturnValue


@dag(start_date=datetime(2022, 12, 1), schedule="@daily", catchup=False)
def sensor_decorator():

    @task.sensor(poke_interval=30, timeout=3600, mode="poke")
    def check_shibe_availability() -> PokeReturnValue:
        r = requests.get("http://shibe.online/api/shibes?count=1&urls=true")
        print(r.status_code)

        if r.status_code == 200:
            condition_met = True
            operator_return_value = r.json()
        else:
            condition_met = False
            operator_return_value = None
            print(f"Shibe URL returned the status code {r.status_code}")

        return PokeReturnValue(is_done=condition_met, xcom_value=operator_return_value)

    # print the URL to the picture
    @task
    def print_shibe_picture_url(url):
        print(url)

    print_shibe_picture_url(check_shibe_availability())


sensor_decorator()
```

### Best practices with Sensors

When using sensors, keep the following in mind to avoid potential performance issues:

- Always define a meaningful timeout parameter for your sensor. The default for this parameter is seven days, which is a long time for your sensor to be running. When you implement a sensor, consider your use case and how long you expect the sensor to wait and then define the sensor's timeout accurately.
- Whenever possible and especially for long-running sensors, use the reschedule mode so your sensor is not constantly occupying a worker slot. This helps avoid deadlocks in Airflow where sensors take all of the available worker slots.
- If your poke_interval is very short (less than about 5 minutes), use the poke mode. Using reschedule mode in this case can overload your scheduler.
- Define a meaningful poke_interval based on your use case. There is no need for a task to check a condition every 60 seconds (the default) if you know the total amount of wait time will be 30 minutes.

### Quiz

Q: A Sensor can be used for (Choose all that apply):
A:
 - waiting for files to appear in an S3 bucket
 - waiting for a task in another DAG to complete
 - waiting for data be present in a SQL table
 - waiting for a specified data and time

Q: You have a sensor that waits for a file to arrive in an S3 bucket. Your DAG runs every 10 mins, and it takes 8 mins to complete.

What is the most appropriate timeout duration for the sensor? (in seconds)
A: 60 * 60

Q: What mode doesn't take a worker slot while a Sensor waits?
A: reschedule

Q: What Sensor(s) can be used to apply logic conditions? (Choose all that apply)
A: PythonSensor and @task.sensor

Q: What parameter can be useful to check for data to be present in a database without putting too much workload on each poke?
A: exponential_backoff


### Key takeaways:

- Sensors wait for an event/condition to be met to complete
- By default, a Sensor times out after 7 days. You should define a better value with the timeout parameter
- A sensor checks an event/condition at every poke_interval (60 seconds by default)
- While a sensor waits, it continuously takes a work slot
- If you have many sensors or expect them to take time before complete, use the reschedule mode
- With the reschedule mode, while a sensor is waiting, its status will be up_for_reschedule
- You can create a sensor with @task.sensor


## Airflow: Command Line Interface (CLI)

- `airflow db init` - initialize metadata database
- `airflow users create`
- `airflow standalone` - only for dev purpose, init db, create user, start scheduler
- `airflow version`
- `airflow info` - get installed packages, version, paths, tools, python version
- `airflow config list`
- `airflow cheat-sheet` - most common commands
- `airflow variables export / import variables.json` - you can export and import
- take note environment variables / configs are not included in exports.

### Testing tasks

As a best practice, each time you add a task in a DAG, test it with:
`airflow tasks test <dag_id> <task_id> <logical date>`

Example: `airflow tasks test cli my_task 2023-01-01`

### Backfill DAGs without the CLI

1. Create backfill DAG

    ```python
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from datetime import datetime

    with DAG(dag_id='backfill_trigger_dag',
            schedule_interval=None,
            start_date=datetime(2022, 1, 1),
            tags=['backfill-trigger-cli'],
            catchup=False) as dag:

        # Use the UI to trigger a DAG run with conf to trigger a backfill, passing in start/end dates and dag_id etc:
        trigger_backfill = BashOperator(
            task_id='trigger_backfill',
            bash_command="airflow dags backfill --reset-dagruns -y -s {{ dag_run.conf['date_start'] }} -e {{ dag_run.conf['date_end'] }} {{ dag_run.conf['dag_id'] }}"
        )

        trigger_backfill
    ```

1.First we shall manually trigger the backfill_trigger_dag with a configuration json from UI. `Trigger DAG w/ config`
1. Pass the necessary parameters in the Configuration JSON for performing the backfill
    `{"dag_id": "example_dag_basic", "date_start": 20230401, "date_end": 20230405}`
1. Select `Unpause DAG when triggered`, then trigger the DAG

### Quiz

Q: What is the purpose of airflow db init and when might you use it?
A: Initializes the Airflow metadata database, typically used when setting up Airflow for the first time

Q: What is the use case for airflow config get-value and how might you use it to troubleshoot issues?
A: Retrieves the value of a specific configuration option, useful for verifying that configuration settings are correctly set

Q: You've recently upgraded your Airflow installation, but now your DAGs is not showing up in the UI. Which commands could you use to identify any import/parsing errors that might be preventing the DAG from being loaded?
A: `airflow dags report`

Q: Why would you use Airflow's backfill functionality?
A: To fill in missing historical data that was not previously captured

Q: What does the airflow db check command do?
A: Checks the connection to the Airflow database


`TODO` Modules not included here:
- UI
- DAGS 101
- DAG Scheduling
- Connections 101
- Variables 101
- Debug DAGs
