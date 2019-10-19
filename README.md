# GAN-Sketcher

This project is based on nvidia SPADE which is a GAN generating photo realistic images from drawings.

This is a fork from https://github.com/noyoshi/smart-sketch
Which is also a fork/based on https://github.com/NVlabs/SPADE

The web-server code has been reworked and cleaned up and the frontend is improved and reimplemented in Vue.js.

![](https://raw.githubusercontent.com/KIDICA/gan-sketcher/master/doc/screen0.png)

## Getting Started

The file structure is mainly inherited but already cleaned up to a certain extend.
The frontend is a vue 

### Prerequisites

You need to install node.js >= 10.x with npm and Python 3.6+. 

### Installation

#### Python



#### Server

We recommend that you install Python 3.7 with the virtual-environment package.

```shell script
sudo apt install python3.7 python3.7-venv -y
```

Clone the repo

```shell script
git clone https://github.com/KIDICA/gan-sketcher.git
```

Install required modules and components.

```shell script
cd server
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start the server.

```shell script
python main.py
```

Now you can open in your browser: http://localhost:9000

#### Frontend

The frontend is a Vue.js application which is entirely separated from the server.

##### Development

```shell script
cd client
npm install 
npm run serve
```

Will provide you will a link to a live recompile entry point.

###### Deployment

This will just deploy the Vue application to app/dist which is statically served by the Python server.

```shell script
cd client
npm run build
```

###### Commands

## Commands

Command                     | Description
----------------------------|---------------------------------------------------------------------------------------
npm run serve               | Real-time compiled dev app for Vue app.
npm run build               | Build the frontend to app/dist
