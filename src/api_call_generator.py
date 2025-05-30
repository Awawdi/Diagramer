import os
import sys

from src.utils import extract_domain_and_alias


class DiagramGenerator:
    """
    A class to generate PlantUML diagrams from templates and API call details.
    """

    @staticmethod
    def generate_api_diagram_from_template(
        template_path: str,
        output_puml_path: str,
        caller_name: str,
        method: str,
        url: str,
        response_code: int
    ) -> str:
        """
        Reads a PlantUML template, injects API call details, and saves the result.
        Returns the generated PlantUML content string.
        """
        domain, target_alias = extract_domain_and_alias(url)

        try:
            with open(template_path, "r") as f:
                template_content = f.read()
        except FileNotFoundError:
            print(f"Error: Template file not found at {template_path}",file=sys.stderr)
            return ""

        # Perform replacements using the extracted values
        final_puml_content = template_content.replace("{{CALLER_NAME}}", caller_name)
        final_puml_content = final_puml_content.replace("{{TARGET_DOMAIN}}", domain)
        final_puml_content = final_puml_content.replace("{{TARGET_ALIAS}}", target_alias)
        final_puml_content = final_puml_content.replace("{{METHOD}}", method.upper())
        final_puml_content = final_puml_content.replace("{{URL}}", url)
        final_puml_content = final_puml_content.replace("{{RESPONSE_CODE}}", str(response_code))

        os.makedirs(os.path.dirname(output_puml_path), exist_ok=True)
        with open(output_puml_path, "w") as f:
            f.write(final_puml_content)

        return final_puml_content