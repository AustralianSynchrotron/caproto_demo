# Caproto Demo

This is a couple of simulated hardwares using caproto, and a matching EpicsQt gui for training purposes.

## Dependencies

Qt EPICS "qegui"
<https://github.com/qtepics/qeBinaries>
(sorry, only for Windows and Centos)

python 3.7 or 3.8
<https://www.python.org/downloads/>

poetry
<https://python-poetry.org/docs/>


## Running it

setup the virtual environment:

```bash
# cd to the directory
poetry config virtualenvs.in-project true --local
poetry update
```

In a command "cmd" window run:

```bash
# cd to the directory
poetry run python demo_ioc.py
```

### GUI (Windows)

To bring up the ui run:

```bat
cd ui
demo_gui_windows.bat
```

### GUI (Centos)

To bring up the ui run:

```bash
cd ui
demo_gui_centos.sh
```

## Troubleshooting

### Conflicting PVs on Network

If more than one person is running this demo on the same network you may see the PV name is already hosted. In this case, change the name in the in the demo_ioc.py, and the gui script.

### No PVs in GUI


Check that your firewall allows ports or python to use the ports.

### Error message

Possibly if you are editting the code you might see an error like;

```txt
Exception has occurred: OSError
[WinError 10038] An operation was attempted on something that is not a socket
```
Refer to further error information in the logger/terminal.

## License

GPL
