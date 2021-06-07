FROM cccs/assemblyline-v4-service-base:latest AS base

ENV SERVICE_PATH dexray.dexray.Dexray

FROM base AS build

USER assemblyline

# Install pip packages
RUN touch /tmp/before-pip
RUN pip install --no-cache-dir --user olefile pycryptodome && rm -rf ~/.cache/pip

USER root
# Remove files that existed before the pip install so that our copy command below doesn't take a snapshot of
# files that already exist in the base image
RUN find /var/lib/assemblyline/.local -type f ! -newer /tmp/before-pip -delete

# change the ownership of the files to be copied due to bitbucket pipeline uid nonsense
RUN chown root:root -R /var/lib/assemblyline/.local

FROM base

COPY --chown=assemblyline:assemblyline --from=build /var/lib/assemblyline/.local /var/lib/assemblyline/.local

# Switch to assemblyline user
USER assemblyline

# Clone Extract service code
WORKDIR /opt/al_service
COPY . .

# Patch version in manifest
ARG version=4.0.0.dev1
USER root
RUN sed -i -e "s/\$SERVICE_TAG/$version/g" service_manifest.yml

# Switch to assemblyline user
USER assemblyline
