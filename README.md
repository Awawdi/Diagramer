Diagramer: Automated API Interaction Diagram Generator

I tried here a POC to generate PlantUML sequence diagrams for API interactions. 
It makes an actual API call to dummyJSON service, extracts relevant details, and then uses a PlantUML template to create a visual representation of the interaction. 
This is very basic implementation that can be extended further


## Features

* **Automated Diagram Generation:** Generates PlantUML diagrams from API call details.
* **Unique Filenames:** Creates uniquely named diagram files for each run (especially useful in CI/CD).
* **API Integration:** Performs a live API call to capture real-time interaction details.
* **Jenkins CI/CD Ready:** Designed to integrate seamlessly into a Jenkins pipeline for automated diagram rendering and archiving.

## How it Works

The core idea is to:

1.  Make an **HTTP API request** (e.g., a `POST` call).
2.  **Extract details** like the target domain, HTTP method, URL, and response status code.
3.  **Inject these details** into a predefined PlantUML template.
4.  **Save the generated PlantUML** `.puml` file.
5.  (Optional, via Jenkins) **Render the `.puml` file into a `.png` image** using a PlantUML Docker container.

---

## Project Structure

```
.
├── Jenkinsfile                   # Jenkins Pipeline definition
├── README.md                     # This file
├── diagrams/                     # Contains PlantUML templates and generated diagrams
│   └── api_interaction_template.puml
├── src/                          # Python source code
│   ├── __init__.py
│   ├── api_call_generator.py     # Class for generating PlantUML content
│   ├── http_requests.py          # (Assumed) Module for making HTTP requests
│   ├── main.py                   # Main script to orchestrate the process
│   └── utils.py                  # Utility functions (e.g., URL parsing, Enums)
└── requirements.txt              # Python dependencies
```

---

## Setup and Local Usage

### Prerequisites

* Python 3.x
* Docker (if you want to render PNGs locally)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Awawdi/Diagramer.git
    cd Diagramer
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running Locally

To generate a `.puml` file based on the configured API call:

```bash
python3 -m src.main
```

This will create a `.puml` file (e.g., `diagrams/api_interaction_diagram_YYYYMMDDHHMMSS.puml`) in the `diagrams/` directory.

To render the `.puml` file into a `.png` image locally (assuming Docker is installed):

```bash
# First, generate the .puml file as shown above
# Then, replace YOUR_UNIQUE_ID with the actual ID from the generated .puml filename
docker run --rm -v $(pwd):/src plantuml/plantuml:1.2024.5 java -jar /plantuml.jar -tpng /src/diagrams/api_interaction_diagram_YOUR_UNIQUE_ID.puml -o /src/diagrams/
```

---

## Jenkins CI/CD Integration

The `Jenkinsfile` in the root of this repository defines a declarative pipeline that automates the entire process:

1.  **`Setup Environment`**: Installs Python dependencies.
2.  **`Generate PlantUML File`**: Executes `src.main` to make the API call and generate the `.puml` file with a unique name (using `BUILD_ID`).
3.  **`Render Diagram`**: Uses a `plantuml/plantuml` Docker image to convert the `.puml` file into a `.png` image.
4.  **`Archive Artifacts`**: Archives both the `.puml` and `.png` files as Jenkins build artifacts.

This setup ensures that a new, updated diagram is generated and archived with every Jenkins build, providing continuous documentation of your API interactions.
