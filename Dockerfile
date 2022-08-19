FROM ubuntu:16.04
MAINTAINER Lawrence Bates <Lawrence.Bates@gmail.com>

RUN mkdir -p /opt/microverse/net-tools/app/static/screenshot && \
chmod -R 770 /opt/microverse/net-tools/app/static/screenshot && \
mkdir /opt/microverse/net-tools/files && \
chmod 770 /opt/microverse/net-tools/files

ENV APP_DIR=/opt/microverse/net-tools
COPY app $APP_DIR/app
COPY files $APP_DIR/files
RUN chmod +x $APP_DIR/files/setpass.sh

WORKDIR $APP_DIR

# Set time zone 
RUN ln -fs /usr/share/zoneinfo/US/Pacific-New /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Install apt packages
RUN apt-get update && apt-get install -y -q --no-install-recommends \
bzip2 curl deborphan dnsutils iputils-ping jq mlocate mtr nano \
openssl openssh-client python-dev python-pip python-setuptools \
sudo supervisor shellinabox telnet traceroute && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# Install pip packages
RUN pip install --upgrade pip && \
pip install -r files/requirements.txt

# Install phantomjs
RUN export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64" && \
tar -xvjf files/$PHANTOM_JS.tar.bz2 && \
mv $PHANTOM_JS /usr/local/share && \
ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin

# Disable shellinabox daemon running at startup, service will be managed by supervisor
RUN sed -i 's/^SHELLINABOX_DAEMON_START=.*/SHELLINABOX_DAEMON_START=0/' /etc/default/shellinabox

# Supervisord configuration
COPY files/supervisord.conf /etc/supervisor/conf.d/
RUN mkdir -p /var/log/supervisor

# Add cloudops user and group
RUN groupadd -f -g 1000 cloudops && \
useradd -g cloudops -s /bin/bash -d /home/cloudops -m -G sudo cloudops

# Set default password, this will be changed via loophole
RUN echo cloudops:cloudops | chpasswd

# Update locate database
RUN updatedb

# Expose ports for net-tools and shellinabox
EXPOSE 4200 5000

# Start shellinabox and run supervisor
CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
