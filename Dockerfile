FROM cccs/assemblyline-v4-service-base:latest

ENV SERVICE_PATH dexray.dexray.Dexray

USER root

# Install any service dependencies here
RUN apt-get update && apt-get install -y perl libcrypt-rc4-perl libdigest-crc-perl libcrypt-blowfish-perl libole-storage-lite-perl 
# Switch to assemblyline user
USER assemblyline

# Copy mobsf service code
WORKDIR /opt/al_service
COPY . .
