# PrivateEquity-Support
PRIVATE EQUITY SUPPORT (PES) is an enterprise  support advisory consulting firm, based out of Nairobi, Kenya. PES is working to successfully originate, de-risk, structure and support Early Stage Financing (SME Investment) in Sub Saharan Africa.


## Development
The following guidelines assume you are using a linux distro.
### Prerequisites
Ensure you have the following installed
 - Python3
 - Pip
 - virtualenv
 - docker


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
### Add environment variables
This project requires certain variables to run. Create a .env file at the roo of your project and add the following variables
```
export SECRET_KEY='a-very-secret-key'
export DJANGO_SETTINGS_MODULE='core.settings.development'
```
export the variables at once using the command. ```source .env```. Ensure you are at the root of the project for this command to work.

## The *Makefile*
The Makefile is special file, that contains shell commands. The utility will help developers to automate commonly run commands and also decrease complexity of certain commands. You can use [this resource](https://makefiletutorial.com/) to learn more. To see what commands are available and how to use them run
```
make help
```

## Dependencies
The app depends on several packages to run such as django. Packages that are essential to run the app are found in the *prod.requirements.txt*.
To install prod dependencies, run:
```
pip install -r prod.requirements.txt
```
Packages that are only required for development such as code styling package **pylint** are found in the *dev.requirements.txt* file.
To install dev dependencies, run:
```
pip install -r dev.requirements.txt
```
The following utility can, however, help you install both during development
```
make install-deps-all
```
### Adding packages
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

## Testing
This project aims to achieve at least 96% code coverage. When developing new features, ensure you code is well tested and takes care of edge cases.
To find out the coverage, you can run the following command:
```
make test-with-coverage
```

## Docker
This project uses docker to separate the application from underlying infrastructure to ease development on any platform. To start a development container, run the following command
```
make dev
```

## Pipelines and Review Apps
 This project is using pipelines and review apps.A pipeline is a group of Heroku apps that share the same codebase.. Each app in a pipeline represents one of the following stages in a continuous delivery workflow:
 ```
                    - Development
                   
                    -  Review
                   
                    -  Staging
                   
                    -  Production
                    

A common pipeline workflow has the following steps:
1.A developer creates a pull request to make a change to the codebase.
2.Heroku automatically creates a review app for the pull request, allowing developers to test the change.
3.When the change is ready, it’s merged into the codebase’s master branch.
4.The master branch is automatically deployed to the pipeline’s staging app for further testing.
5.When the change is ready, a developer promotes the staging app to production, making it available to the app’s end users.

You can use [this resource](https://devcenter.heroku.com/articles/pipelines/) to learn more.```


Navigate to [localhost port 8000](0.0.0.0:8000) to view your app.

Happy coding!