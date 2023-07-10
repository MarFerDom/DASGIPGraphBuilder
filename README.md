# DASGIP Graph Builder <a id="top"></a>

Easly build graphs from Eppendorf - DASGIP MultiparallelBioreactorSystem generated .csv files.

<img src=https://media3.giphy.com/media/ZaxcauVgBidVaBYdN2/giphy.gif width=640 style="text-align: center"><br>

A graphical web interface for generating graphs for **DASGIP MBS** output. Configuration of limits and colors are saved persistently.
Uploaded data and generated graphs are stored for a period of time.
The app works as a locally hosted website using [Flask](https://flask.palletsprojects.com/en/2.3.x/).
Graphs are generated using [matplotlib](https://matplotlib.org/) with a non-GUI backend.

<br>

***
*This project was requested to help improve the efficiency of scientists working with the DASGIP MBS and is open to other research groups and companies.*
***
<br>
<br>

## Content in this file:
* [Requirements](#req)
* [Installation](#install)
* [Usage](#usage)
    * [CLI](#cli)
    * [Web App](#web_app)
    * [Batch file](#batch_file)
* [TODO](#todo)
* [Components](#comp)
    * [Application Configuration](#app_conf)
    * [Graph generation](#graph)
    * [States](#states)
    * [Controller](#control)
    * [UI](#ui)
* [Architecture](#arch)
    * [Plugins](#plugins)
    * [Config](#config)
* [Project Requirements](#proj_req)
* [Author](#author)

## Requirements <a id="req"></a>

- Python 3.8.x
- Flask 2.3.2
- Flask-Dropzone 1.6.0
- matplotlib 3.7.1
- numpy 1.24.4
- pandas 2.0.3

[back to top](#top)

## Installation <a id="install"></a>

```
pip install -r requirements.txt
```

[back to top](#top)

## Usage <a id="usage"></a>
> <br>
> There are some options for using the program:
> <br>
> <br>


### CLI <a id="cli"></a>

> <br>
> <code>DASGIPGraphBuilder</code> is a simple CLI.
> <br>
> <br>

<img src=https://user-images.githubusercontent.com/16342417/252313957-c1f60f19-b47c-4ddb-b1e0-b4a9df800bcf.PNG width=800><br>

- From the main folder, run:

```
   python -m src.DASGIPGraphBuilder <FILENAME> [-s vessel_number] [-d variable, [...]]
```

[back to top](#top)

### Web App <a id="web_app"></a>

> <br>
> <code>app</code> is a Flask web server version.
> <br>
> <br>

<img src=https://user-images.githubusercontent.com/16342417/252301437-76611394-1310-4923-a063-89178fe49837.png width=480><br>

- From the main folder, run:

```
   python -m src.app
```

- If no file is available, the main page will redirect to upload automatically.

<img src=https://user-images.githubusercontent.com/16342417/252301645-e47c4ab2-8241-4898-9092-c473945c4a9d.png width=480><br>

- From the main page files, sources within files and options can be selected.

- The options menu allows for the selection of variables, their color scheme and plot limits.

![Options Menu](https://media3.giphy.com/media/QO9QHPHu2xDSOKbHot/giphy.gif)

After uploading files and setting prefered options, graphs are easily generated at the click of a button.

![Generating graphs](https://media3.giphy.com/media/ZaxcauVgBidVaBYdN2/giphy.gif)

[back to top](#top)

### Batch file <a id="batch_file"></a>

> <br>
> <code>run.sh</code> is a bash file that creates a virtual environment on first use and runs the web server in it.
> <br>
> <br>

From the main folder, run:

```
   ./run.sh
```

[back to top](#top)

## TODO <a id="todo"></a>

    0. Improve graphics for portability.

    1. Include admin interface for configuring app behaviour.

    2. Add more graph configurations options.

    3. Load from compressed file.

[back to top](#top)




## Components <a id="#comp"></a>


### Application Configuration <a id="app_conf"></a>

    * conf.py contains constants and sets logging.

    * protocols.py contains interfaces expected by modules.


### Graph generation: <a id="graph"></a>

    1. DASGIP_loader:

        Implements all tasks related to the internal organization of the CSV.

    2. graph_maker: 

        Implements all graph related operations.
    
    3. handler:

        Interface for building graph from file and configuration
        settings using a loader module and a grapher module.

    4. os_ops:

        Implements all OS and time related tasks.

### Storage: <a id="storage"></a>

    Implements presistent memory as a json file to:

    - Store only relevant data content from the file;
    - Exclude data entries after configurable time;
    - Exclude generated images after configurable time;
    - Store graph configuration settings.

### UI: <a id="ui"></a>

    1. DASGIPGraphBuilder:
    
        A simple CLI using argparse.
        
    2. app:
    
        A local web server application using Flask.

[back to top](#top)

## Project requirements: <a id="proj_req"></a>

1 - The program must run locally on a Mac and not depend on remote assets or servers.

2 - The program must create graphs for selected variables in subplots for each file/vessel.

3 - Graphs must be easily configured for color and y-axis limits.

4 - Graphs are subject to tinkering and subjective evaluation.

[back to top](#top)

## Author

> [MarFerDom](https://github.com/MarFerDom) - [linkedin](https://www.linkedin.com/in/marc-dom/).

[back to top](#top)
