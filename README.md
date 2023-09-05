
## Digital Sewa
An app for Dialer support
## Features

- Ticket creation on **incoming call**
- Filtering tickets aginst
- Agent creation and different status like On Call, On Break
- Click to call from tickets itself
- Log generation for every call



## Installation

Get the app

```bash
bench get-app digital_sewa {github_url} --branch version-14
```

Install the digital_sewa app

```bash
  bench --site{site_name} Install-app digital_sewa
```

## Configuration




Go To Servetel


![Logo](https://digitalsewa.nestorhawk.com/files/1.png)

Copy the token from here and paste it in dialer settings Authorizatiion

![Logo](https://digitalsewa.nestorhawk.com/files/8%20(1).png)

Copy the Number from my Number section

![Logo](https://digitalsewa.nestorhawk.com/files/3.png)

and paste it in caler id

![Logo](https://digitalsewa.nestorhawk.com/files/8%20(1).png)


Now You can create agents in Servetel

![Logo](https://wiki.nestorbird.com/files/9.png)

And with same data you also need to create agent in erp side

![Logo](https://wiki.nestorbird.com/files/5.png)

Now you are good to go when someone call on caller id new DS ticket will be created if exists or else
it will create new DS ticket

![Logo](https://wiki.nestorbird.com/files/10.png)

## Logs

Break Logs

![Logo](https://wiki.nestorbird.com/files/11.png)

Agent Logs

![Logo](https://wiki.nestorbird.com/files/12.png)

Webhook Configuration

![Logo](https://wiki.nestorbird.com/files/13.png)
