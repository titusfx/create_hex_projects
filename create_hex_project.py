import os
import click

# Define the CLI using Click
@click.group()
def cli():
    pass

# Command to generate the project structure
@cli.command()
@click.argument('project_name')
def init_project(project_name):
    """
    Initializes the project structure for a given project name.
    """
    base_structure = {
        f'{project_name}/': ['application', 'domain', 'infrastructure', 'interfaces'],
        f'{project_name}/domain/': ['models', 'exceptions', 'repositories', 'services'],
        f'{project_name}/infrastructure/': ['adapters', 'cache', 'db', 'repositories', 'services'],
        f'{project_name}/interfaces/': ['api_rest/'],
        f'{project_name}/interfaces/api_rest/': ['models', 'routes'],
        'tests/': [f'{project_name}/'],
        f'tests/{project_name}/': ['domain', 'interfaces']
    }
    
    # Create directories
    for path, subdirs in base_structure.items():
        for subdir in subdirs:
            dir_path = os.path.join(path, subdir)
            os.makedirs(dir_path, exist_ok=True)  # Create subdirectories

    # Create __init__.py files for all directories
    for path in base_structure.keys():
        for root, dirs, _ in os.walk(path):
            for dir in dirs:
                init_path = os.path.join(root, dir, '__init__.py')
                open(init_path, 'a').close()  # 'a' to ensure we don't overwrite existing files

    click.echo(f'Project {project_name} has been initialized successfully.')

if __name__ == '__main__':
    cli()

