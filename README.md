# NMLab final project : Housing Agency System
**Consortium Blockchain** for housing agency to share real-time information and to record housing transactions. Built with Python and React for the user interface.
![image](https://github.com/CynthiaYLiu/blockchain-housing-agency/blob/master/img/home.png)

* This project was developed by [Cynthia Liu](https://github.com/CynthiaYLiu), [Pierre Sue](https://github.com/PierreSue), and [Danny Tsai](https://github.com/dannyInc).<br>
* More details in poster: https://github.com/CynthiaYLiu/blockchain-housing-agency/blob/master/report/Fianl_poster.pdf
* Demo video: https://www.youtube.com/watch?v=ujUNZ1e1UBQ&feature=youtu.be


## Functions



## How to run this project?

### Server
It is required to install some libraries on your computer in advance. (ex.numpy, ecdsa... )
First, we should open the control panel of servers.
```bash
$ cd control_panel
$ bash run.sh
```

Then open four terminals to run four servers (which should be set by real estate agents).
```bash
$ cd real_estate_agents
$ bash run1.sh
```
```bash
$ cd real_estate_agents
$ bash run2.sh
```
```bash
$ cd real_estate_agents
$ bash run3.sh
```
```bash
$ cd real_estate_agents
$ bash run4.sh
```

### Client
If the client and server are not on the same host, we should change the 'HOST' into server's fixed IP address in client/client.py . <br>
Please install **Flask** first !

* Run Backend
```bash
$ flask run 
```

* Run Frontend
```bash
$ cd react-frontend
$ npm install
$ npm start
```
And then you can browse our website!
