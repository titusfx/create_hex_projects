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
        f'{project_name}/': ['application/', 'domain/', 'infrastructure/', 'interfaces/'],
        f'{project_name}/application/': ['__init__.py'],
        f'{project_name}/domain/': ['__init__.py', 'models/', 'exceptions/', 'repositories/', 'services/'],
        f'{project_name}/infrastructure/': ['__init__.py', 'adapters/', 'cache/', 'db/', 'repositories/', 'services/'],
        f'{project_name}/interfaces/': ['api_rest/'],
        f'{project_name}/interfaces/api_rest/': ['__init__.py', 'models/', 'routes/'],
        'tests/': ['__init__.py', f'{project_name}/'],
        f'tests/{project_name}/': ['domain/', 'interfaces/']
    }
    
   # Create directories
    for path, subdirs in base_structure.items():
        os.makedirs(path, exist_ok=True)  # Ensure the root directory exists
        for subdir in subdirs:
            dir_path = os.path.join(path, subdir)
            os.makedirs(dir_path, exist_ok=True)  # Create subdirectories
            # Create an __init__.py file if the subdir is not a file path
            if not subdir.endswith('.py'):
                init_path = os.path.join(dir_path, '__init__.py')
                open(init_path, 'a').close()
            
    # Create __init__.py files for all directories
    for root, dirs, files in os.walk(project_name):
        for dir in dirs:
            init_path = os.path.join(root, dir, '__init__.py')
            open(init_path, 'a').close()  # 'a' to ensure we don't overwrite existing files

    click.echo(f'Project {project_name} has been initialized successfully.')

if __name__ == '__main__':
    cli()
