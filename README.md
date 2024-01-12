# Poetry containers 

## Description

I wanted to compare different solutions for installing packages using poetry in containers.  
For me, the most important metric was the size of the container, but the simplicity of execution might also be important for some users.  
I do not measure time spent on build because it is dependent on the speed of the internet (cache is one of the options to measure it, and I will probably use it in the next iteration)

**Note**: I do not use `poetry build` or install the wheel package in any container. In my opinion, it is pointless because it doesn't contain all the required packages

## Preparation

I created a simple TODO app with tests and used additional tools like code formatter ([black](https://github.com/psf/black)) and code coverage counter ([coverage.py](https://coverage.readthedocs.io/en/7.4.0/)).  
It is all to simulate a real type of application.
Each part of the test has the exact requirements:
One container must contain packages from the "develop" group to allow tests to run inside the container.
One container is free from packages in the "develop" group containers (like a production container image) just to run the app.
Each "production" container must run with a dedicated used

Under each test, you can find a table that describes:
- Type - is the "production" or "test" image
- Dockerfile - path to the dockerfile
- Command - command to execute if you want to build an image
- Size - the size of the created container
- Diff - the difference in the size of the build container to the base image 
- All commands are described in the [Taskfile.yaml](Taskfile.yaml), which is a dedicated file for (Task)[https://taskfile.dev] project  


## Tests of containers

### All in

The simple solution assumes you install all packages + poetry in the same container.
In that case, you can use poetry inside the container, but you must also remember that poetry and its dependencies are heavy.  
In this scenario, also all packages are created in virtualenv (which is not required)


| Type       | Dockerfile                                                     | Command                              | Size   | Diff    | 
|------------|----------------------------------------------------------------|--------------------------------------|--------|---------|
| Test       | [Dockerfile_all_in_tests](dockerfiles/Dockerfile_all_in_tests) | `task container:build:all-in`        | 302 MB | +171 MB |
| Production | [Dockerfile_all_in_prod](dockerfiles/Dockerfile_all_in_prod)   | `task container:build:all-in:no-dev` | 288 MB | +157 MB |


### Multi-stage build with virtualenv

This example shows how to build a virtualenv with required packages and use the virtualenv in another stage.  
With this scenario, we can see how powerful it is to use separate images just for poetry.

| Type       | Dockerfile                                                 | Command                               | Size   | Diff   | 
|------------|------------------------------------------------------------|---------------------------------------|--------|--------|
| Test       | [Dockerfile_venv_tests](dockerfiles/Dockerfile_venv_tests) | `task container:build:venv-mv`        | 160 MB | +29 MB |
| Production | [Dockerfile_venv_prod](dockerfiles/Dockerfile_venv_prod)   | `task container:build:venv-mv:no-dev` | 152 MB | +21 MB |


### Multi-stage build with exported requirements

Another multi-stage build pattern; this time, requirements are exported and directly installed inside the system.
I believe this solution might be the easiest for most users and give very nice results.


| Type       | Dockerfile                                                                               | Command                              | Size   | Diff   | 
|------------|------------------------------------------------------------------------------------------|--------------------------------------|--------|--------|
| Test       | [Dockerfile_export_requirements_tests](dockerfiles/Dockerfile_export_requirements_tests) | `task container:build:export`        | 164 MB | +33 MB |
| Production | [Dockerfile_export_requirements_prod](dockerfiles/Dockerfile_export_requirements_prod)   | `task container:build:export:no-dev` | 149 MB | +18 MB |


## Conclusion

As you can see, Poetry is a "heavy" tool". However, the benefits of using it are too high to drop it.
Fortunately, a simple multi-stage build, with a grouping of the dependencies, can signify improved container size.  
Regarding production images, the smallest one is this from the 3rd scenario (but the 2nd has only +3 MB).

## Bonus

If you are looking for all **production** ready Dockerfile, you can look at [Dockerfile](dockerfiles/Dockerfile).
There, you can find all the steps that help you to make tests, export them to a separate directory, and finally build the production image.
The size of this image is the same as in 3rd scenario. However, this is the most complicated example.

Commands to use this example:
- `task container:build`
- `task container:build:test`

# Thank you and have a great day!
