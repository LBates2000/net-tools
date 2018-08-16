# net-tools
A microservice that returns a response containing the output of remote shell commands or scripts. Used to troubleshoot region-specific issues. 

The service Includes an API endpoint, a web front end that provides links to a set of network tools, and an embedded web console that allows shell access via a browser.

* Container exposes a RESTful API for the 'net-tools' microservice on http port 5000 using [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.5/). 
* The service returns the output of commands on the "allowed" list (currently [curl](http://manpages.ubuntu.com/manpages/xenial/en/man1/curl.1.html), [dig](http://manpages.ubuntu.com/manpages/xenial/en/man1/dig.1.html), [mtr](http://manpages.ubuntu.com/manpages/xenial/en/man8/mtr.8.html), [nslookup](http://manpages.ubuntu.com/manpages/xenial/en/man1/nslookup.1.html), [phantomjs](http://phantomjs.org/documentation/), [ping](http://manpages.ubuntu.com/manpages/xenial/en/man8/ping.8.html), [traceroute](http://manpages.ubuntu.com/manpages/xenial/man1/traceroute.db.1.html)). This can be expanded to return the ouput of _any_ command or script that returns a response.
* The container also hosts a web-based shell console ([shellinabox](https://code.google.com/archive/p/shellinabox/)) at `http://net-tools.microverse.systems:4200` and through a service redirect from `http://net-tools.microverse.systems:5000/shellinabox` 
* The service responds to both [GET](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) and [POST](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html) methods and returns output as [`mimetype=text/plain`](https://tools.ietf.org/html/rfc2854) so that the response can be embedded in a webpage.

## Examples:
```
curl http://net-tools.microverse.systems:5000/shellcommand -d 'command=nslookup' -d 'parameters=dogpile.com'
Server:         192.168.65.1
Address:        192.168.65.1#53

Non-authoritative answer:
Name:   dogpile.com
Address: 54.231.114.97

Non-authoritative answer:
Name:   www.dogpile.com
Address: 54.231.185.7

curl http://net-tools.microverse.systems:5000/shellcommand -d 'command=mtr' -d 'parameters=-rw dogpile.com'
Start: Wed Nov 16 01:24:15 2016
HOST: 7b25ad17035b                       Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- 172.17.0.1                          0.0%    10    0.2   0.1   0.1   0.2   0.0
  2.|-- s3-website-us-east-1.amazonaws.com  0.0%    10    0.7   1.0   0.7   1.7   0.0


curl http://net-tools.microverse.systems:5000/shellcommand -d 'command=dig' -d 'parameters=dogpile.com'

; <<>> DiG 9.10.3-P4-Ubuntu <<>> dogpile.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 10660
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 4, ADDITIONAL: 5

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;dogpile.com.                   IN      A

;; ANSWER SECTION:
dogpile.com.            5       IN      A       54.231.112.186

;; AUTHORITY SECTION:
dogpile.com.            48794   IN      NS      ns-604.awsdns-11.net.
dogpile.com.            48794   IN      NS      ns-1326.awsdns-37.org.
dogpile.com.            48794   IN      NS      ns-1689.awsdns-19.co.uk.
dogpile.com.            48794   IN      NS      ns-446.awsdns-55.com.

;; ADDITIONAL SECTION:
ns-1326.awsdns-37.org.  149406  IN      A       205.251.197.46
ns-1689.awsdns-19.co.uk. 157532 IN      A       205.251.198.153
ns-446.awsdns-55.com.   153262  IN      A       205.251.193.190
ns-604.awsdns-11.net.   162310  IN      A       205.251.194.92

;; Query time: 10 msec
;; SERVER: 192.168.65.1#53(192.168.65.1)
;; WHEN: Wed Nov 16 01:28:21 UTC 2016
;; MSG SIZE  rcvd: 257
```
