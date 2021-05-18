FROM cccs/assemblyline-v4-service-base:latest

ENV SERVICE_PATH dexray.dexray.Dexray

USER root

# Install any service dependencies here
RUN apt-get update && apt-get install -y perl libcrypt-rc4-perl libdigest-crc-perl libcrypt-blowfish-perl libole-storage-lite-perl wget
RUN mkdir -p /opt/al_support
RUN wget -O /opt/al_support/dexray.pl https://raw.githubusercontent.com/Ewifly/assemblyline-service-dexray/main/dexray/dexray.pl

RUN chmod +x /opt/al_support/dexray.pl
# Switch to assemblyline user
USER assemblyline

# Copy mobsf service code
WORKDIR /opt/al_service
COPY . .
