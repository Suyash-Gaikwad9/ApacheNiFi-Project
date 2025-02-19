**I. Project Setup and Docker Compose:**

1.  **Create Project Directory:\
    > **

2.  Bash

mkdir simple-project \# Creates the project directory

cd simple-project \# Navigates into the directory

3.  

4.  *Explanation:* This sets up the main project folder where all the
    > configuration files and data will reside.

5.  **Create Subdirectories:\
    > **

6.  Bash

mkdir spark data \# Creates subdirectories for Spark scripts and data

mkdir data/input \# Creates the input directory for NiFi

7.  

8.  *Explanation:* spark will hold your Python Spark script, and
    > data/input will be where NiFi places the generated files.

9.  **Create** docker-compose.yml**:\
    > **

10. Bash

touch docker-compose.yml \# Creates an empty docker-compose.yml file

vim docker-compose.yml \# Opens the file in the vim editor (or use your
preferred editor)

11. 

12. *Explanation:* docker-compose.yml is the core configuration file
    > that defines the services (NiFi and Spark) and their interactions.

13. **Populate** docker-compose.yml**:** Paste the following content
    > into docker-compose.yml (using vim or your editor):

14. YAML

version: \'3\' \# Optional, can be removed

services:

nifi:

image: apache/nifi:1.23.2 \# Or your specific tag

ports:

\- \"8443:8443\" \# Expose HTTPS port for NiFi

volumes:

\- ./data:/data \# Mount data directory

environment:

\- NIFI_SECURITY_ENABLED=false \# Disable security (for this demo only)

spark:

image: bitnami/spark:3.5.0 \# Or your specific tag

volumes:

\- ./spark:/app \# Mount Spark scripts directory

\- ./data:/data \# Mount data directory

depends_on: \# Spark starts after NiFi

\- nifi

command: sleep infinity \# Keeps the Spark container running

15. 

16. *Explanation:* This YAML file defines two services: nifi and spark.
    > It specifies the Docker images to use, port mappings, volume
    > mounts, and environment variables. depends_on ensures Spark starts
    > *after* NiFi.

17. **Create Spark Script (**wordcount.py**):\
    > **

18. Bash

touch spark/wordcount.py \# Creates the Python script file

vim spark/wordcount.py \# Opens the file in vim (or your editor)

19. 

20. *Explanation:* This creates the Python script that will perform the
    > word count.

21. **Populate** wordcount.py**:** Paste the following code into
    > wordcount.py:

22. Python

from pyspark.sql import SparkSession

spark =
SparkSession.builder.appName(\"SimpleWordCount\").master(\"local\[\*\]\").getOrCreate()

try:

text_files = spark.read.text(\"/data/input/\*\") \# Read files from the
input directory

words = text_files.selectExpr(\"explode(split(value, \' \')) as word\")
\# Split lines into words

word_counts = words.groupBy(\"word\").count() \# Count word occurrences

print(\"\\n=== WORD COUNTS ===\")

word_counts.show() \# Display the results

print(\"===================\\n\")

except Exception as e:

print(f\"Error processing data: {e}\")

finally:

spark.stop() \# Stop the Spark session

23. 

24. *Explanation:* This Python script uses Spark to read text files from
    > the /data/input directory, splits each line into words, counts the
    > occurrences of each word, and prints the results.

25. **Start Docker Containers:\
    > **

26. Bash

docker-compose up -d

27. 

28. *Explanation:* This command starts the NiFi and Spark containers in
    > detached mode (running in the background). The -d flag is
    > important so your terminal is not blocked.

**II. NiFi Flow Configuration:**

1.  **Access NiFi UI:\
    > \
    > ** Open your web browser and go to https://localhost:8443. Accept
    > the security warning (it\'s safe for this local test).

2.  **Add Processors:\
    > \
    > ** Drag and drop two processors onto the canvas: GenerateFlowFile
    > and PutFile.

3.  **Connect Processors:\
    > \
    > ** Drag the connection icon from GenerateFlowFile to PutFile to
    > create a connection.

4.  **Configure** GenerateFlowFile**:\
    > **

    -   Right-click -\> Configure.

    -   Scheduling tab: Set \"Run Schedule\" (e.g., 30 sec).

    -   Properties tab: Set \"Custom Text\" (e.g., \"Hello Spark Hello
        > NiFi Hello Docker\").

    -   Apply.

5.  **Configure** PutFile**:\
    > **

    -   Right-click -\> Configure.

    -   Properties tab: Set \"Directory\" to /data/input. Set \"Conflict
        > Resolution\" to replace.

    -   Apply.

6.  **Start Processors:\
    > \
    > ** Right-click on each processor -\> Start.

**III. Running Spark Job:**

1.  **Check Data Generation:\
    > **

2.  Bash

ls data/input \# Check if NiFi is creating files in the input directory

3.  

4.  

5.  **Run Spark Job:\
    > **

6.  Bash

docker exec -it simple-project-spark-1 spark-submit /app/wordcount.py

7.  

8.  *Explanation:* This command executes the spark-submit command
    > *inside* the Spark container, running your wordcount.py script.
    > Replace simple-project-spark-1 with your Spark container name if
    > it\'s different (use docker ps to check).

9.  **View Results:\
    > \
    > ** The word counts will be printed in your terminal.

**IV. Stopping and Restarting:**

1.  **Stop Containers:\
    > **

2.  Bash

docker-compose down

3.  

4.  

5.  **Start Containers (and reload NiFi flow):\
    > **

6.  Bash

docker-compose up -d

7.  

8.  After restarting, you\'ll need to re-import the NiFi flow if you
    > didn\'t save it as a template.

**V. Key Commands and Explanations:**

-   mkdir: Create directory.

-   cd: Change directory.

-   touch: Create an empty file.

-   vim (or your editor): Edit a file.

-   docker-compose up -d: Start Docker containers in detached mode.

-   docker-compose down: Stop and remove Docker containers.

-   docker ps: List running Docker containers.

-   docker exec -it \<container_name\> \<command\>: Execute a command
    > inside a Docker container.

-   docker-compose logs \<service_name\>: View logs for a Docker Compose
    > service.

-   ls -l: List files and directories with details.

-   mv: Move files or directories.

-   chmod +x \<file\>: Make a file executable (used for testing file
    > permissions).

This detailed list should help you practice and demonstrate the NiFi and
Spark setup effectively. Remember to explain the purpose of each command
and the configuration files during your demonstration. Good luck!
