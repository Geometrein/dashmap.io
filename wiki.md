# 🎊 Welcome to the Dashmap wiki!
### Overview
##### What is Dashmap?
DashMap is an open source web platform that gathers, analyses and visualises urban data.

##### What is Dashmap made of?
DashMap is an isolated Plot.ly.Dash app wrapped in a parent Flask app. This allows utilizing the highly customizable Flask app to serve the Plotly dashboards without paying a hefty fee for Dash Enterprise license. You get the best of both worlds. The ease of creating dashboards with Plotly and the rich features of Flask. Of course, there are tradeoffs but for the current scale of the application, these are insignificant.
##### Pros:
- Flask and Dash apps can be modified, styled and developd separately!
- Quick dashboards with Plotly/dash
- All Flask features (Flask-Login, Flask-Admin, Flask-Assets).
##### Cons:
- Performance
- Python infused front end is not ideal.

---

### Installation
Set up a virtual environment:
```
python3 -m venv venv
```


Activate the virtual environment:
```
source venv/bin/activate
```

Install requirements.txt
```
pip install -r requirements.txt
```

Create a .env file with variable "MAPBOX_TOKEN" and assign your [Mapbox](https://docs.mapbox.com/help/getting-started/access-tokens/) token to it. 

You're all set 🚀

---

### File structure
```
dashmap.io
│   README.md
│   main.py                       # Main app
│   gunicorn_config.py            # gunicorn configuration file
│   requirements.txt
│   LICENSE
└───tests                         # Unittests
│   │   test_basics.txt           # Basic response checks
└───website                       # Main website  folder
│   │   __init__.py               # Initialises all apps and configurations 
│   │   views.py                  # Flask app views
│   └───dashmap                   # Dash app folder (see below)
│   └───data                      #  Datasets 
│   └───static                    #  Static assets for the Flask app
│   └───templates                 #  html templates utilised by Flask 
│       │   base.html             #  base templates for all pages
│       │   home.html             #  Home page 
│       │   support.html          #  Support page

# Dash app
└───dashmap                       # Dash app folder
│    └───assets                   # Static assets for The Dash app
│    └───layouts                  # Defines the basic app layout
│    └───callbacks                # Defines the basic app callbacks
│   map.py                        # Initialises the Dash app inside flask
│   map_callbacks.py              # Initialises the callbacks for Dash app 
│   map_graphs.py                 # Initialises non-callback generated graphs for dash app
│   map_layout.pyy                # Initialises the basic app layout
```
---

### Contributing to Dashmap
We would love to see your input!
We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

#### All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase.
We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue that pull request!


#### Report bugs using Github's [issues](https://github.com/Geometrein/dashmap.io/issues)
We use GitHub issues to track public bugs. Report a bug by opening a new issue.
Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give a sample code if you can.
- What you expected would happen
- What actually happens

We *love* thorough bug reports.
#### License
By contributing, you agree that your contributions will be licensed under its MIT License. In short, when you submit code changes, your submissions are understood to be under the same [MIT License](https://github.com/Geometrein/dashmap.io/blob/main/LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.