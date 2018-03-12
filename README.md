```
 __
/\ \__                        __
\ \ ,_\    __     _ __   ___ /\_\    ___     ____    ___    ___   _____      __
 \ \ \/  /'__`\  /\`'__\/'___\/\ \  / __`\  /',__\  /'___\ / __`\/\ '__`\  /'__`\
  \ \ \_/\ \L\.\_\ \ \//\ \__/\ \ \/\ \L\ \/\__, `\/\ \__//\ \L\ \ \ \L\ \/\  __/
   \ \__\ \__/.\_\\ \_\\ \____\\ \_\ \____/\/\____/\ \____\ \____/\ \ ,__/\ \____\
    \/__/\/__/\/_/ \/_/ \/____/ \/_/\/___/  \/___/  \/____/\/___/  \ \ \/  \/____/
                                                                    \ \_\
                                                                     \/_/
```

> A simple tool to look at the sky with a PiKon Telescope (a newtonian tube).

Getting Started
---------------

- Ensure you have virtualenvwrapper setup and a new project is setup for you to workon.

```
$ pip install virtualenvwrapper
$ source `which virtualenvwrapper.sh`
```

This will create the folder `$HOME/.virtualenvs`. Then you need to create a project:

```
$ mkvirtualenv tarcioscope
```

Once this repo is cloned, you will need to execute

```
$ workon tarcioscope
```

Then upgrade packaging tools and install dependencie with its testing requirements:

```
$ pip install --upgrade pip setuptools
$ pip install -r requirements.txt
```
