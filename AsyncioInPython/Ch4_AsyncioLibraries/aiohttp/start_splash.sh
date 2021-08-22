#! /bin/bash -e

# Pulls the scrapinghub Splash contaienr and starts it, exposing the port 8050
# Splash is a javascript rendering service - necessary to effectively web-scrape modern webpages.

docker pull scrapinghub/splash
exec docker run --rm -d -p 8050:8050 scrapinghub/splash
