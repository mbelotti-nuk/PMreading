# PMreading
 Project for reading PM paritcles with raspberry pi
 
![20250320_171447](https://github.com/user-attachments/assets/85c64c1a-4345-4fc9-b960-b1f4552d6f13)


I have installed a PM sensor in my home and made up a script to read the values and publish them on a local website hosted by a raspberry pi.

* The sensor is available here https://www.amazon.it/dp/B07YXSGVR4?ref=ppx_yo2ov_dt_b_fed_asin_title

To make the website you should install nginx locally on your raspberry pi (i've followed this tutorial https://www.youtube.com/watch?v=Y1mNeWwj8D0&t=8s) and move to `/var/www/html` the `index.html` and `server.py` files. In these two files, you should change the IP address with the one corresponding to your raspberry pi.
Then just execute the `server.py` script to perform measurement and update the local website.

The website during measurements:




https://github.com/user-attachments/assets/502b5102-bb2d-4c56-b10e-7ad3113ad238


