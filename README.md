# Internet-Based-Systems-Architecture
Web application used to ease the access of Instituto superiror Técnico resources information, by means of web site, mobile applications or QR-Codes.

The project was developed for the course [ASINT](https://fenix.tecnico.ulisboa.pt/disciplinas/ASInt77/2019-2020/1-semestre) from my masters program at Instituto Superior Técnico(IS).

In this project we implemented an application to acess information about [IST](https://tecnico.ulisboa.pt/pt/) resources (buildings, rooms, services, people, canteen).

The system implemented is divided in the following components:

- FENIX API : Origin of the data that is available to users.
- Microservices : Small web-services that are responsible for managing the requests for the corresponding resource.
- Backend : A set of public API and web pages that allow the access and manipulation of the various resources.
- Admin Web pages : A set of pages that allow the administrator to mange and edit some of the resources.
- Mobile access : a simple application that can be executed in a mobile phone that allows users to acces the resources information.
- Log : receive and store all the accesses to every components.

