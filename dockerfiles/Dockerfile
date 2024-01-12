# This part of the build is used to export the requirements to a separate file
FROM python:3.10.12-slim-bullseye@sha256:2daf07926ccdff5dbeef6bee46cc5bb07322f417c102609601177a1559156385 AS builder

RUN apt-get update \
 && apt-get install --yes curl

ENV POETRY_VERSION=1.7.1  PATH="${PATH}:/root/.local/bin"

COPY poetry.lock pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python3 - \
 && poetry export --output=requirements.txt \
 && poetry export --output=requirements-dev.txt --only dev

# This one step takes the exported requirements and copies them from 1st step
FROM python:3.10.12-slim-bullseye@sha256:2daf07926ccdff5dbeef6bee46cc5bb07322f417c102609601177a1559156385 AS app_builder

RUN useradd --create-home todoapp
USER todoapp
WORKDIR /home/todoapp

COPY example_application ./example_application
COPY --from=builder requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

# These two steps are used to run all tests and export the result of the test to the host machine
# (it is helpful inside CI/CD platforms, to show the results)
FROM app_builder AS test_runner
COPY example_application_tests ./example_application_tests
COPY --from=builder requirements-dev.txt ./requirements-dev.txt

RUN pip3 install -r requirements-dev.txt \
 && mkdir reports  \
 && python3 -m coverage run -m pytest -vvv example_application_tests --junitxml=reports/test_report.xml \
 && python3 -m coverage xml -o reports/coverage_report.xml \
 && python3 -m coverage report


FROM scratch AS export_test_results
COPY --from=test_runner /home/todoapp/reports .

# Result of build
FROM app_builder

EXPOSE 8000
CMD python3 -m uvicorn example_application.main:app --host 0.0.0.0
