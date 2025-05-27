import os
import datetime

from src.api_call_generator import DiagramGenerator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, os.pardir) # Go up one level from 'src'

TEMPLATE_FILE = os.path.join(PROJECT_ROOT, "diagrams", "api_interaction_template.puml")
BASE_OUTPUT_PUML_NAME = "api_interaction_diagram"


def main():
    """
    Main function to orchestrate the diagram generation process.
    Generates a unique filename for the output diagram.
    """
    unique_id = os.getenv('BUILD_ID')
    if not unique_id:
        unique_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    unique_output_puml_file = os.path.join(
        PROJECT_ROOT, "diagrams",
        f"{BASE_OUTPUT_PUML_NAME}_{unique_id}.puml"
    )
    unique_output_png_file = os.path.join(
        PROJECT_ROOT, "diagrams",
        f"{BASE_OUTPUT_PUML_NAME}_{unique_id}.png"
    )

    caller = "MyOrchestrationService"
    api_method = "POST"
    api_url = "https://dummyjson.com/auth/login"
    api_response = "200 OK"

    generated_puml_content = DiagramGenerator.generate_api_diagram_from_template(
        template_path=TEMPLATE_FILE,
        output_puml_path=unique_output_puml_file,
        caller_name=caller,
        method=api_method,
        url=api_url,
        response_code=api_response
    )

    # Print statements now reside in main, documenting the unique filename
    print(f"PlantUML diagram saved to: {unique_output_puml_file}")
    print(f"Expected PNG output at: {unique_output_png_file}")
    print("\nGenerated PlantUML Content (from template):\n")
    print(generated_puml_content)

if __name__ == "__main__":
    main()