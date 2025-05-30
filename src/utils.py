import sys
from enum import Enum
from urllib.parse import urlparse

def extract_domain_and_alias(url: str) -> tuple[str, str]:
    """
    Extracts the domain and a PlantUML-safe alias from a URL.
    Returns a tuple: (domain_name, plantuml_alias)
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        cleaned_domain = domain.replace("www.", "")
        base_alias = cleaned_domain.split(':')[0].replace(".", "_")
        plantuml_alias = ''.join(c for c in base_alias if c.isalnum() or c == '_')

        # If alias is empty or starts with a non-alphabetic character, prefix it
        if not plantuml_alias or not plantuml_alias[0].isalpha():
            plantuml_alias = "Service_" + plantuml_alias if plantuml_alias else "ExternalService"
            if plantuml_alias[0] == '_':
                plantuml_alias = "Service" + plantuml_alias
        return domain, plantuml_alias

    except Exception as e:
        print(f"Warning: Could not parse URL '{url}' with error: {e}", file=sys.stderr)
        return url, "GenericService"

class APIMethods(Enum):
    """
    Enum for HTTP methods used in API calls.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"