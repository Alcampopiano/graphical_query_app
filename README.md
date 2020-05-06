# Graphical Query Application

<img src="https://github.com/Alcampopiano/graphical_query_app/blob/master/img/ga.gif?raw=true" alt="drawing" width="1000"/>

---

This is an example of using the [Anvil App Server](https://pypi.org/project/anvil-app-server) 
to build a web application using nothing but Python.

As shown above, this application allows you to select data based on a graphical-style query.

## Installation

```
$ pip install -r graphical_query_app/requirements.txt
```

## Running the app locally

After cloning this repository, run the following command to launch the app 

```
$ anvil-app-server --app graphical_query_app
```

The app should now be running on http://localhost:3030. 

## Using your own data

I have included some same data in the "example_data" directory. Feel free to load that into the
app to see how everything works. When you are ready to use your own data, make sure it is squeaky clean!
That is, don't have mixed types inside the same column. Numbers need to be able to be treated as numbers.
Also, best to keep your column names sane as well
(no spaces or special characters, or else the app may explode)

## Saving queries

To save your queries, simply click "save query" once you have one that you like.
A text area will appear asking you to give it a nice description. That's it!
Now you can reuse that query without having to construct it all over again.

Enjoy!


