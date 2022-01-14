# PrivateEquity-Support
PRIVATE EQUITY SUPPORT (PES) is an enterprise  support advisory consulting firm, based out of Nairobi, Kenya. PES is working to successfully originate, de-risk, structure and support Early Stage Financing (SME Investment) in Sub Saharan Africa.


## Development
The following guidelines assume you are using a linux distro.
### Prerequisites
Ensure you have the following installed
 - Python
 - Pip
 - virtualenv


### Clone the repository
Run the following command to clone the repository
```
git clone https://github.com/margaret254/PrivateEquity-Support.git
```
After cloning change into the directory like so:
```
cd PrivateEquity-Support
```
### Create a virtual environment
You need a virtual environment to manage dependencies for this project. Create a virtual environment with whatever name you prefer e.g.
```
virtualenv venv
```
Activate the virtualenv with the following command
```
source venv/bin/activate
```

## The *Makefile*
The Makefile is special file, that contains shell commands. The utility will help developers to automate commonly run commands and also decrease complexity of certain commands. You can use [this resource](https://makefiletutorial.com/) to learn more. To see what commands are available and how to use them run
```
make help
```

## Adding packages
This project intends to keep development and production packages separate

To install a dev package, run the following command:
```
make add-package-dev package=package_name
```
for example, to install pylint, you would run;  ```make add-package-dev package=pylint```

Similarly, to install production packages, run the following
```
make add-package-prod package=package_name
```

Happy coding!