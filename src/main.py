import json
import os
import datetime

from src import http_requests
from src.api_call_generator import DiagramGenerator
from src.utils import APIMethods

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, os.pardir) # Go up one level from 'src'

TEMPLATE_FILE = os.path.join(PROJECT_ROOT, "diagrams", "api_interaction_template.puml")
BASE_OUTPUT_PUML_NAME = "api_interaction_diagram"

def generate_unique_filenames(base_name: str) -> tuple[str, str, str]:
    """
    Generates unique filenames for the PlantUML and PNG outputs.
    Uses Jenkins BUILD_ID if available, falls back to a timestamp.
    :param: base_name: Base name for the output files.
    :return: (unique_id, puml_filepath, png_filepath).
    """
    unique_id = os.getenv('BUILD_ID')
    if not unique_id:
        unique_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    puml_filepath = os.path.join(
        PROJECT_ROOT, "diagrams",
        f"{base_name}_{unique_id}.puml"
    )
    png_filepath = os.path.join(
        PROJECT_ROOT, "diagrams",
        f"{base_name}_{unique_id}.png"
    )
    return unique_id, puml_filepath, png_filepath

def main():
    """
    Main function to orchestrate the diagram generation process.
    """
    unique_id, unique_output_puml_file, unique_output_png_file = generate_unique_filenames(BASE_OUTPUT_PUML_NAME)

    # Example API call details
    caller = "MyOrchestrationService"
    api_url = "https://dummyjson.com/auth/login"
    header = {"Content-Type": "application/json"}
    payload = json.dumps({"username": "emilys", "password": "emilyspass", "expiresInMins": 30})

    try:
        response = http_requests.post_with_retry(url=api_url,
                                             headers=header,
                                             data=payload,
                                             verify=False)
    except Exception as ex:
        print(f"API call failed: {str(ex)}")
        return

    generated_puml_content = DiagramGenerator.generate_api_diagram_from_template(
        template_path=TEMPLATE_FILE,
        output_puml_path=unique_output_puml_file,
        caller_name=caller,
        method=APIMethods.POST.value,
        url=api_url,
        response_code=response.status_code
    )

    print(f"PlantUML diagram saved to: {unique_output_puml_file}")
    print(f"Expected PNG output at: {unique_output_png_file}")
    print("\nGenerated PlantUML Content (from template):\n")
    print(generated_puml_content)

if __name__ == "__main__":
    main()