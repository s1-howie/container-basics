# Use the official Apache image from the Docker Hub
FROM httpd:2.4

# Copy your html file to the default Apache document root
COPY index.html /usr/local/apache2/htdocs/

# NOTE:  ou do not need a CMD instruction here because the base httpd image already contains a CMD that runs Apache in the foreground.