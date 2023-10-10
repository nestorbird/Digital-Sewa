# Digital Sewa Introduction

##### Digital Sewa 
Ticketing Solution in Frappe and ERPNext complemented by the power of Voice Services.

Digital Sewa serves as a versatile extension for Frappe, ERPNext, or Custom App doc types, allowing easy configuration of Digital Sewa Tickets to track and log call records handled by agents, whether for inbound or outbound calls. The app seamlessly integrates with two leading Cloud Voice service providers, Servertel and Knowlarity, to offer robust voice call capabilities within the Frappe ecosystem.

### Features
- Realtime data capturing on Incomming Call
- Click to Call from Agent screen to Customer
- Multiple Agent handling
- Break Management for Agent
- Break Log of each agent with Report
- Agent Productivity Report
- Ticketing Solution extending any ERPNext DocType 

### Compatibality
Frappe v13 (all)
Frappe v14 (all)

# Installation Guide

**1.  Over Frappe Cloud**
Simply signup with Frappe Cloud for a free trial and create a new site. Select Frappe Version-13 and select [**ERPNext**](https://frappecloud.com/marketplace/apps/erpnext) and [**Digital Sewa**](https://frappecloud.com/marketplace/apps/digital_sewa) from Frappe MarketPlace to Install. You can get started in a few minutes with a new site and a fresh install to try out the simple and cool features of the App.

**2. Manual Installation (Self hosted)**
Once you've set up a Frappe site, installing Digital Sewa is simple:
- Download the app using the Bench  
```sh
 bench get-app --branch <branch name> https://github.com/nestorbird/Digital-Sewa.git
```
- Replace <branch name> with the appropriate branch as per your setup

| Branch | Depedency |
| ------ | ------ |
| digital_sewa-crm| Need CRM module from ERPNext version-13 & version-14 |
| digital_sewa-support| This is an independent module, works with Frappe version-13 & version-14 |
- Install the app on your site.

```
bench --site <site name> install-app digital_sewa
```

#### External Pre-requsite
- Access to [Servertel](https://customer.servetel.in/login) with API features enabled.

#### Internal Pre-requisute
- Agent Created in Servertel with same created in Digital Sewa (Agent DocType)

### Depedencies for Digital Sewa
Digital Sewa with branch digital_sewa-crm is dependent on ERPNext with CRM module for any both version 13 and 14.
Digital Sewa with branch digital_sewa-support is an independent module that can be directly installed on Frappe version 13 and 14, and has no depedencies.
**Digital Sewa for Voice calling has 2 Integrations with** 
- Servertel
- Knowlarity

## Contributing
- [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
- [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)

## License
                                  
[GNU General Public License (v3)](https://github.com/nestorbird/Digital-Sewa/blob/digital-sewa-support/license.txt)

## Support
For support please visit or click [here](https://wiki.nestorbird.com/wiki/support)
