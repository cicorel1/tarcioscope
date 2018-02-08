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

- Change directory into your newly created project.

    cd tarcioscope

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
