# Pacloud

## Context

This project was created by VARLEZ Pierre, BAL-PETRE Olivier, and FARO Juliette for their 3rd year project at the IT Tallaght.

## The project

Package managers are an essential part of any Linux distribution: they allow to install, update or remove software on your computer. This software is distributed by using packages, which contain the executable software as well as various informations, including the dependencies to other packages, the version number and other elements useful for the installation or maintenance.  

Most package managers use binary packages compiled for generic hardware as it's fast to install. However, they can include useless dependencies. Some package managers, as [Portage](https://wiki.gentoo.org/wiki/Portage), build the packages from source code according to the user hardware and parameters. This makes light-weight and hardware-optimized packages. The downside of this type of package managers is the long installation time due to the compilation.  

This project aims to create a package manager that would use Cloud computing to compile packages that would be optimized for your hardware.

## Server

The server side was entirely created with CloudFormation to be deployed quickly in the AWS Cloud. More information about the architecture and the deployment can be found in [the server README.md](./AWS).

## Client

The client was created with Python 3 to be highly portable. More information about the client can be found in [the client README.md](./pacloud)

