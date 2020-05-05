# Graphical Query Application

<img src="https://github.com/Alcampopiano/graphical_query_app/blob/master/img/ga.gif?raw=true" alt="drawing" width="1000"/>

An example of using the Anvil App Server to build a web application using nothing but Python.

As shown above, this application allows you to select data based on a graphical-style query.

## Setup and installation

```
$ conda create -n my_env
$ conda activate my_env
$ conda install pip
$ conda install -c anaconda pandas
$ pip install https://anvil-public-assets.s3.amazonaws.com/runtime-preview-utoX6sie/anvil-runtime-preview.bin.tgz
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

## Adding example queries

You will only need to do this if (1) you want to extend the application to work with multiple users and (2)
you want them to have some pre-built queries when they open the app. 

One way to add an example query is to use the `--shell` option as follows:

```
$ anvil-app-server --app graphical_query_app --shell
```

This will drop you inside a Python prompt where you can use the
[Anvil DataTables API](https://anvil.works/docs/data-tables)
to access the app's database.

Let's add a simple example query from the shell. Oh, and for now don't worry about the long query string, it just
tells the app how to display the graphical query on the screen (i.e., it holds button colors and text, and pandas query fragments). 

```python
query_str='{"but_text":["EQAO_Math_Program","equal to","Academic","and","math_eqao_03","less than",3],"but_color":\
["#ff7f0e","#1f77b4","#9467bd","#2ca02c","#ff7f0e","#1f77b4","#9467bd"],"query_frags":\
["EQAO_Math_Program","==","\"Academic\"","&","math_eqao_03","<","3"]}'

user_id='example'

notes="Students who were below the provincial standard in grade three \
but went on to be in the Academic Math program (in grade 9)"

app_tables.saved_queries.add_row(user_id=user_id, query_str=query_str, notes=notes)
```

Now when you visit the app, the "example queries" section will have the above query
all ready to go. As I mentioned above though, for a single user, it is much
easier to just use saved queries.

Enjoy!


