# PMreading
 Project for reading PM paritcles with raspberry pi


I have installed a PM sensor in my home and made up a script to read the values and publish them on a local website hosted by a raspberry pi.

* The sensor is available here https://www.amazon.it/dp/B07YXSGVR4?ref=ppx_yo2ov_dt_b_fed_asin_title

To make the website you should install nginx locally on your raspberry pi (i've followed this tutorial https://www.youtube.com/watch?v=Y1mNeWwj8D0&t=8s) and move to `/var/www/html` the `index.html` and `server.py` files. In these two files, you should change the IP address with the one corresponding to your raspberry pi.

The website during measurements

