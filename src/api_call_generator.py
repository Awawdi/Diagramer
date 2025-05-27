import os
from utils import extract_domain_and_alias


TEMPLATE_FILE = "../diagrams/api_interaction_template.puml"
OUTPUT_PUML_FILE = "../diagrams/api_interaction_diagram.puml"

def generate_api_diagram_from_template(
    template_path: str,
    output_puml_path: str,
    caller_name: str,
    method: str,
    url: str,
    response_code: str = "200 OK"
):
    """
    Reads a PlantUML template, injects API call details, and saves the result.
    """
    # Use the utility function to get domain and alias
    domain, target_alias = extract_domain_and_alias(url)

    # Read the template file
    try:
        with open(template_path, "r") as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {template_path}")
        return

    # Perform replacements using the extracted values
    final_puml_content = template_content.replace("{{CALLER_NAME}}", caller_name)
    final_puml_content = final_puml_content.replace("{{TARGET_DOMAIN}}", domain)
    final_puml_content = final_puml_content.replace("{{TARGET_ALIAS}}", target_alias)
    final_puml_content = final_puml_content.replace("{{METHOD}}", method.upper())
    final_puml_content = final_puml_content.replace("{{URL}}", url)
    final_puml_content = final_puml_content.replace("{{RESPONSE_CODE}}", response_code)

    # Save the content to a .puml file
    os.makedirs(os.path.dirname(output_puml_path), exist_ok=True)
    with open(output_puml_path, "w") as f:
        f.write(final_puml_content)

    print(f"PlantUML diagram saved to: {output_puml_path}")
    print("\nGenerated PlantUML Content (from template):\n")
    print(final_puml_content)

if __name__ == "__main__":
    # Simulate an API call details
    caller = "MyOrchestrationService"
    api_method = "POST"
    api_url = "https://dummyjson.com/auth/login"
    api_response = "200 OK"

    # Generate the PlantUML file using the template and constants
    generate_api_diagram_from_template(
        TEMPLATE_FILE, # Used the constant here
        OUTPUT_PUML_FILE, # Used the constant here
        caller,
        api_method,
        api_url,
        api_response
    )