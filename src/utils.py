# src/utils.py

from urllib.parse import urlparse

def extract_domain_and_alias(url: str) -> tuple[str, str]:
    """
    Extracts the domain and a PlantUML-safe alias from a URL.
    Returns a tuple: (domain_name, plantuml_alias)
    """
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Create a PlantUML-safe alias: remove www., replace dots with underscores, remove port
        target_alias = domain.replace("www.", "").replace(".", "_").split(':')[0]

        # Ensure alias starts with a letter and is alphanumeric
        if not target_alias:
            target_alias = "ExternalAPI" # Fallback if domain is empty

        # If alias starts with a number or invalid char, prepend 'A'
        if target_alias and not target_alias[0].isalpha():
            target_alias = "A" + target_alias

        # Remove any non-alphanumeric characters (except underscore)
        target_alias = ''.join(c for c in target_alias if c.isalnum() or c == '_')

        return domain, target_alias
    except Exception as e:
        print(f"Warning: Could not parse URL '{url}'. Error: {e}. Using generic names.")
        return url, "ExternalAPI" # Fallback in case of parsing errors