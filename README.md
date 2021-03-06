tarcioscope
===

> A simple tool to look at the sky with a PiKon Telescope (a newtonian tube).

What you will need
---

- [A Raspberry Pi](https://www.raspberrypi.org/)
- [A Raspberry Pi Camera](https://www.raspberrypi.org/products/camera-module-v2/)
- A microSD card with Linux installed
  - I'm using [Raspbian](https://www.raspbian.org/)
- Python 3
- ngnix 1.4

Getting Started
---

- Ensure you have virtualenvwrapper setup and a new project is setup for you to workon.

```bash
pip install virtualenvwrapper
source `which virtualenvwrapper.sh`
```

This will create the folder `$HOME/.virtualenvs`. Then you need to create a project:

```bash
mkvirtualenv tarcioscope
```

Once this repo is cloned, you will need to execute

```bash
workon tarcioscope
```

Then upgrade packaging tools and install dependencies:

```bash
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

To run the project, simply go from the project's root:

```bash
./bin/tarcioscope
```

It will start a webserver on port 8000 binding to all IP addresses.

Note on nginx
---

The way I'm running this project is having the server part running on port 8000 and [the client running as a SPA](https://github.com/tarciosaraiva/tarcioscope-ui) being served by ngnix on port 80.

What I also have is an [nginx configuration](nginx.config) that redirects every call to `/api` to my Python web server running on port 8000.

I found this to be the ideal setup so then I don't have to worry about CORS headers et al.

Contributing
---

- Fork it
- Work on it
- Send me a pull request
