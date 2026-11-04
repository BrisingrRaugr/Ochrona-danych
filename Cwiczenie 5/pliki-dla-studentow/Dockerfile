FROM httpd:2.4-alpine
RUN apk add --no-cache python3
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY www/ /usr/local/apache2/htdocs/
COPY dane/ /lab-data/
COPY cgi-bin/ /usr/local/apache2/cgi-bin/
RUN chown -R root:daemon /lab-data \
    && chmod 755 /lab-data \
    && chmod 640 /lab-data/ogolny.txt \
    && chmod 600 /lab-data/poufny.txt \
    && find /usr/local/apache2/cgi-bin -type f -name '*.cgi' -exec chmod 755 {} \;
