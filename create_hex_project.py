import os
import click


# Define the CLI using Click
@click.group()
def cli():
    pass


# Descriptions for each directory
descriptions = {
    "application": (
        "# This application layer acts as the orchestrator for the flow of data between the "
        "domain and infrastructure layers. It contains application logic and business rules "
        "that coordinate tasks using the domain models. For example, it might include a "
        "module for processing new user registrations, where it would use domain services "
        "to verify user data and infrastructure services to store the user."
    ),
    "domain": (
        "# The domain layer is the heart of the business logic. It encapsulates the business "
        "rules, models, and exceptions that define the operations and constraints of the "
        "business domain. For instance, a 'User' model would be defined here with methods "
        "for verifying passwords and updating user details."
    ),
    "domain/models": (
        "# Domain models represent the core business objects within the application. They "
        "include classes that model the business concepts, their data, and behavior. For "
        "example, in an e-commerce application, you would have models like 'Product', "
        "'Cart', and 'Order' defined here with their respective properties and methods."
    ),
    "domain/exceptions": (
        "# This package contains custom exceptions that are specific to the domain logic. "
        "These exceptions handle cases that are outside the normal flow of the application, "
        "such as 'ProductNotFoundException' or 'PaymentDeclinedException', which are thrown "
        "when a product cannot be found in the catalog or when a user's payment method is declined."
    ),
    "domain/repositories": (
        "# Repositories within the domain layer are interfaces that abstract the retrieval "
        "of domain objects from data stores. They define the methods needed to query and "
        "persist domain entities. For example, an 'OrderRepository' might declare methods "
        "like 'find_by_id' and 'save' which would be implemented in the infrastructure layer."
    ),
    "domain/services": (
        "# Domain services contain additional logic that doesn’t fit within a domain model. "
        "This includes complex business rules or processes that span multiple domain models. "
        "For example, a 'PaymentProcessingService' could coordinate between 'Order', 'Payment', "
        "and 'Notification' models to process a user's payment."
    ),
    "infrastructure": (
        "# The infrastructure layer provides implementations for the interfaces defined in the "
        "domain layer. It typically includes data access logic, file storage logic, and external "
        "API clients. For example, this is where you would implement 'SQLUserRepository' which "
        "handles database operations for 'User' entities using SQL."
    ),
    "infrastructure/adapters": (
        "# Adapters in the infrastructure layer serve as the bridge between the application and "
        "the external services or databases. They implement the interfaces defined in the domain "
        "layer to provide concrete functionality. For instance, an adapter could implement the "
        "'IEmailService' interface using a third-party email service provider."
    ),
    "infrastructure/cache": (
        "# The cache package includes classes and configurations for caching mechanisms to improve "
        "performance. For example, it might contain a 'RedisCacheAdapter' that uses Redis to cache "
        "common queries or results."
    ),
    "infrastructure/db": (
        "# This package is dedicated to database configurations, connection management, and migrations. "
        "It contains the setup needed to connect to a SQL or NoSQL database and might include scripts "
        "or tools like Alembic to handle database versioning and migrations."
    ),
    "infrastructure/repositories": (
        "# Here you'll find the concrete implementations of the repository interfaces defined in the "
        "domain layer. These implementations are specific to the data storage solutions being used, "
        "such as a 'MongoDBOrderRepository' for storing orders in MongoDB."
    ),
    "infrastructure/services": (
        "# The services package within the infrastructure layer contains implementations of services "
        "like message queuing, file storage, and third-party clients. For example, an 'S3StorageService' "
        "would provide methods to save and retrieve files from AWS S3."
    ),
    "interfaces": (
        "# The interfaces layer defines the contracts for how external entities interact with the "
        "application. This includes RESTful APIs, GraphQL endpoints, and CLI interfaces. They are "
        "adapters that translate between the application's internal domain models and the external "
        "representation of data."
    ),
    "interfaces/api_rest": (
        "# This package contains all the components needed to build a RESTful API interface. It defines "
        "route handlers, request/response schemas, and the necessary configuration to expose the API to clients."
    ),
    "interfaces/api_rest/models": (
        "# API REST Models are the schemas that represent how data is sent and received over the API. "
        "They define the structure of request bodies and response payloads. For example, a 'UserRequestModel' "
        "might define the expected fields when creating a new user."
    ),
    "interfaces/api_rest/routes": (
        "# Routes within the API REST package define the endpoints available to clients and handle the incoming "
        "requests. They call upon the application services to perform actions and return responses. A route such "
        "as '/users/{id}' would be defined here to handle user-related operations."
    ),
}

output_folder = "generated_projects"  # Folder to contain all generated projects


# Command to generate the project structure
@cli.command()
@click.argument("project_name")
def setup_project_structure(project_name):
    init_project(project_name, output_folder)
    click.echo(f"Project {project_name} has been initialized successfully.")


def init_project(project_name, output_folder="."):
    """
    Initializes the project structure for a given project name.
    """

    project_path = os.path.join(
        output_folder, project_name
    )  # Path to the specific project

    base_structure = {
        f"{project_path}/": ["application", "domain", "infrastructure", "interfaces"],
        f"{project_path}/domain/": ["models", "exceptions", "repositories", "services"],
        f"{project_path}/infrastructure/": [
            "adapters",
            "cache",
            "db",
            "repositories",
            "services",
        ],
        f"{project_path}/interfaces/": [
            "api_rest/",
            "graphql/",
            "cli/",
        ],
        f"{project_path}/interfaces/api_rest/": ["models", "routes"],
        f"{output_folder}/tests/": [f"{project_name}/"],
        f"{output_folder}/tests/{project_name}/": ["domain", "interfaces"],
    }

    # Create directories
    for path, subdirs in base_structure.items():
        for subdir in subdirs:
            dir_path = os.path.join(path, subdir)
            os.makedirs(dir_path, exist_ok=True)  # Create subdirectories

    # Create __init__.py files for all directories
    for path, subdirs in base_structure.items():
        for subdir in subdirs:
            dir_path = os.path.join(path, subdir)
            if os.path.isdir(dir_path):  # Only proceed if it's a directory
                init_file = os.path.join(dir_path, "__init__.py")
                with open(init_file, "w") as f:
                    # Write the description to the __init__.py file
                    # Determine the key for the descriptions dictionary
                    description_key = os.path.relpath(dir_path, project_path)
                    f.write(
                        descriptions.get(
                            description_key,
                            "# No specific description for this package.\n",
                        )
                    )

    click.echo(f"Project {project_path} has been initialized successfully.")


# Function to check if Poetry is installed
def is_poetry_installed():
    try:
        subprocess.run(
            "poetry --version",
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


import subprocess
import os

import json


# New command to create environment
@cli.command()
@click.argument("project_name", default="my_project")
def create_environment(project_name):
    """
    Installs and sets up a new project environment with Poetry, Commitizen, and pre-commit inside the generated_projects folder.
    """
    click.echo(
        """Installs and sets up a new project environment with Poetry, Commitizen, and pre-commit inside the generated_projects folder."""
    )

    project_path = os.path.join(output_folder, project_name)

    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Check if Poetry is already installed, install if not
    if not is_poetry_installed():
        # Install Poetry globally (requires user to have curl installed)
        subprocess.run(
            "curl -sSL https://install.python-poetry.org | python -",
            shell=True,
            check=True,
        )

    # Navigate to the output folder and start a new project with Poetry
    os.chdir(output_folder)
    subprocess.run(f"poetry new {project_name}", shell=True, check=True)

    # Navigate to the project directory
    os.chdir(project_name)

    # Install development dependencies
    subprocess.run(
        "poetry add --group dev commitizen pre-commit", shell=True, check=True
    )

    # Initialize Git and set up Commitizen
    subprocess.run("git init", shell=True, check=True)
    subprocess.run("poetry run cz init", shell=True, check=True)
    # subprocess.run("poetry run cz init --yes", shell=True, check=True)

    # Configure git alias
    subprocess.run(
        "git config --global alias.cz '!poetry run cz commit'", shell=True, check=True
    )

    # Initialize pre-commit and make initial commit
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run("git cz", shell=True, check=True)

    # Call the init_project function to set up the project structure
    init_project(project_name)

    click.echo(
        f"Environment for {project_name} has been set up successfully in {project_path}."
    )


if __name__ == "__main__":
    cli()
