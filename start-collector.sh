#!/bin/bash

# Copy the crontab template
cp /app/crontab.template /etc/cron.d/collector

# Set proper permissions for the crontab file
chmod 0644 /etc/cron.d/collector

# Apply cron job
crontab /etc/cron.d/collector

# Create the log file to redirect cron output
touch /var/log/cron.log

# Start cron daemon in the foreground
cron

# Keep container running and output logs
tail -f /var/log/cron.log 