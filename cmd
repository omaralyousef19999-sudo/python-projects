C:\Users\Owner>nmap -sV 192.168.10.111
Starting Nmap 7.99 ( https://nmap.org ) at 2026-07-19 14:09 +0300
Nmap scan report for 192.168.10.111
Host is up (0.00034s latency).
Not shown: 986 closed tcp ports (reset)
PORT     STATE    SERVICE          VERSION
53/tcp   filtered domain
135/tcp  open     msrpc            Microsoft Windows RPC
139/tcp  open     netbios-ssn      Microsoft Windows netbios-ssn
445/tcp  open     microsoft-ds?
1025/tcp open     msrpc            Microsoft Windows RPC
1026/tcp open     msrpc            Microsoft Windows RPC
1030/tcp open     oracle           Oracle Database
1032/tcp open     iad3?
1033/tcp open     netinfo?
1034/tcp open     oracle-tns       Oracle TNS Listener (error: 12550)
2179/tcp open     vmrdp?
7070/tcp open     ssl/realserver?
8080/tcp open     http             PHP cli server 5.5 or later (PHP 8.2.15)
8081/tcp open     blackice-icecap?
3 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port1032-TCP:V=7.99%I=7%D=7/19%Time=6A5CB0A8%P=i686-pc-windows-windows%
SF:r(oracle-tns,8,"\0\x08\0\0\x0b\0\0\0");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port1033-TCP:V=7.99%I=7%D=7/19%Time=6A5CB0A8%P=i686-pc-windows-windows%
SF:r(oracle-tns,8,"\0\x08\0\0\x0b\0\0\0");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port8081-TCP:V=7.99%I=7%D=7/19%Time=6A5CB090%P=i686-pc-windows-windows%
SF:r(GetRequest,24,"HTTP/1\.1\x20404\x20Not\x20Found\r\n\r\nNot\x20found\.
SF:")%r(FourOhFourRequest,24,"HTTP/1\.1\x20404\x20Not\x20Found\r\n\r\nNot\
SF:x20found\.")%r(SIPOptions,28,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\
SF:nBad\x20request\.")%r(HTTPOptions,24,"HTTP/1\.1\x20404\x20Not\x20Found\
SF:r\n\r\nNot\x20found\.")%r(RTSPRequest,24,"HTTP/1\.1\x20404\x20Not\x20Fo
SF:und\r\n\r\nNot\x20found\.");
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 141.99 seconds
