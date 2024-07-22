# an intermediate build stage to avoid having poetry and its dependencies in the final image
FROM python:3.11-slim as requirements-stage

# 
WORKDIR /tmp

# install poetry
RUN pip install poetry

# copy the poetry dependency files
COPY ./pyproject.toml ./poetry.lock* /tmp/

# export the dependencies into a requirements.txt file
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 
FROM python:3.11-slim

# set maintainer information
LABEL maintainer="Shabel Gumah <shabel500@gmail.com>"

# set the working directory
WORKDIR /app

# copy requirements.txt from initial poetry build stage
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# install all dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy source code
COPY ./src /app/src

# create non-root user to run the application
RUN useradd --create-home appuser
RUN chown -R appuser /app
USER appuser

# start the dev server
CMD ["fastapi",  "dev", "src/main.py"]