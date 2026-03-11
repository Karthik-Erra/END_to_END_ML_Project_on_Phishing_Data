from setuptools import setup, find_packages

required_packages = []

def get_requirements(file_path):
    with open(file_path,'r') as file_obj:
        packages = file_obj.readlines()
        required_packages = [packages.replace('\n','').strip() for packages in lines if packages != '-e .']
        return required_packages
    
setup(
    name = 'NetworkSecurity',
    version = '0.0.1',
    author = 'Karthik',
    author_email = 'Karthikerra67@gmail.com',
    packages = find_packages(),
    install_packages = get_requirements('requirements.txt')
)