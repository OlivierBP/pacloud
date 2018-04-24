# pacloud

This is the folder where everything client-related should be.  

[pacloud](./pacloud) contains the files relative to the command-line interface  
[web](./web) contains the files relative to the web interface  
[libpacloud](./libpacloud) contains the files relative to the micro-services and the API that makes the package manager what it is  
[etc](./etc) contains a template of the user configuration. It is to be copied in /etc/pacloud/  

This project uses python setuptools to be built. To build it, use:
```
# pip install -e .
```
on this folder.
