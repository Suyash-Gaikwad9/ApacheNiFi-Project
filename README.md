```markdown
# NiFi-Spark Word Count Pipeline (Dockerized)

This project demonstrates a simple data pipeline using Apache NiFi for data ingestion and Apache Spark for data processing, all containerized with Docker Compose.  It's designed for educational purposes and showcases the basic integration of NiFi and Spark.

## Overview

The pipeline performs a word count on text data.  NiFi generates the text data and places it in a shared directory. Spark then reads the data from this directory, performs the word count, and prints the results.

## Prerequisites

*   Docker Desktop (or Docker Engine) installed and running
*   A text editor (e.g., VS Code, Sublime Text, Atom)

## Project Structure

```
simple-project/
├── docker-compose.yml       # Docker Compose configuration
├── spark/
│   └── wordcount.py        # Spark Python script
└── data/
    └── input/             # Directory for NiFi generated files
```

## Setup and Execution

1.  **Clone the Repository (If applicable):**

    ```bash
    git clone <repository_url>
    cd simple-project
    ```

2.  **Start Docker Containers:**

    ```bash
    docker-compose up -d
    ```

3.  **Access NiFi UI:**

    Open your web browser and go to `https://localhost:8443`. Accept the security warning (this is a self-signed certificate for local testing).

4.  **Configure NiFi Flow:**

    *   Drag and drop two processors: `GenerateFlowFile` and `PutFile`.
    *   Connect `GenerateFlowFile` to `PutFile`.
    *   Configure `GenerateFlowFile`:
        *   Scheduling tab: Set "Run Schedule" (e.g., `30 sec`).
        *   Properties tab: Set "Custom Text" (e.g., "Hello Spark Hello NiFi Hello Docker").
        *   Apply.
    *   Configure `PutFile`:
        *   Properties tab: Set "Directory" to `/data/input`. Set "Conflict Resolution" to `replace`.
        *   Apply.
    *   Start both processors.

5.  **Run Spark Job:**

    ```bash
    docker exec -it simple-project-spark-1 spark-submit /app/wordcount.py
    ```

    (Replace `simple-project-spark-1` with your Spark container name if different - use `docker ps` to check).

6.  **View Results:**

    The word counts will be printed in your terminal.

## Stopping the Containers

```bash
docker-compose down
```

## Key Commands

*   `docker-compose up -d`: Starts the containers.
*   `docker-compose down`: Stops the containers.
*   `docker ps`: Lists running containers.
*   `docker exec -it <container_name> <command>`: Executes a command inside a container.
*   `docker-compose logs <service_name>`: Views logs for a service.

## Code Explanation

### `docker-compose.yml`

This file defines the NiFi and Spark services, their dependencies, port mappings, and volume mounts.  The `NIFI_SECURITY_ENABLED=false` setting disables NiFi security for this demonstration.

### `wordcount.py`

This Python script uses PySpark to:

1.  Read text files from the `/data/input` directory.
2.  Split each line into words.
3.  Count the occurrences of each word.
4.  Print the word counts.

## Important Notes

*   This project is for demonstration and learning purposes.
*   NiFi security is disabled for simplicity. In a production environment, you *must* configure proper security.
*   The self-signed certificate used by NiFi is only for local testing.  Do not use it in a production environment.

## Further Development

*   Explore more advanced NiFi processors and Spark transformations.
*   Implement error handling and logging.
*   Integrate with other data sources and sinks.
*   Implement proper security for NiFi and Spark.

## License

[Choose a license - e.g., MIT License]
```

This README file provides a good starting point for your GitHub repository.  Remember to replace the placeholders (e.g., `<repository_url>`, `[Choose a license]`) with the correct information.  You can also add more details or sections as needed.
