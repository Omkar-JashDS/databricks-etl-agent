# Databricks ETL Agent

An AI system that converts ETL mapping documents into executable Databricks pipelines.

## Tech Stack
* Streamlit
* Python
* PySpark
* LLM & Prompt Engineering
* Terraform

## Architecture & Workflow

```mermaid
flowchart TD
    subgraph S1["1. Ingestion"]
        A[User Input / Document Upload]
    end

    subgraph S2["2. Requirements Agent"]
        B[Parser Agent]
        C{Missing Info?}
        D[Clarification Questions]
        E[Output JSON]

        B --> C
        C -- Yes --> D
        D -- User Answers --> B
        C -- No --> E
    end

    subgraph S3["3. Validation Gate"]
        V[JSON Schema Check]
        V_Check{Valid?}

        E --> V
        V --> V_Check
        V_Check -- No --> D
    end

    subgraph S4["4. Sample Data Review"]
        F[PySpark Mock Engine]
        G{User Approved?}

        V_Check -- Yes --> F
        F --> G
        G -- Rejected --> B
    end

    subgraph S5["5. Databricks Pipeline"]
        H[Base Pipeline Template]
        I[Configured Databricks Pipeline]

        H --> I
    end

    A --> B
    G -- Approved --> H
    ```