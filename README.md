# linear-stats-to-notion

a python script gathering data from Linear regarding tickets, bug in particular or past cycles, and generates Notion documents

## Prerequisite
### On Notion side
A [Notion account](https://www.notion.so/) (no constraint on the subscription plan, it works with the free plan).

A Notion integration with the rights of **consulting**, **creating** or **editing content** (no need concerning the comments or the user's data are necessary).<br/>
Visit [this page](https://www.notion.so/my-integrations) to create such integration.<br>


<span style="color: #377B2A">**Note.**</span> Once this integration is created, you will need the secret key of the integration that has been generated (section "Secret keys")

#### To launch an analysis on the tickets
A database on Notion that contains the following columns:
* `Name` (type title)
* `Date of Inspection` (type date)
* `Generation Method` (type select)
* `Nb Tickets` (type number)

#### To launch an analysis on the bugs
A database on Notion that contains the following columns:
* `Name` (type title)
* `Date of Inspection` (type date)
* `Generation Method` (type select)
* `Nb Tickets` (type number)

#### To launch an analysis on the bugs
A database on Notion that contains the following columns:
* `Name` (type title)
* `Date of Inspection` (type date)
* `Generation Method` (type select)
* `Cycle` (type number)

Finally, you have to add the Notion integration you have created to the database(s) corresponding to the analysis you plan to launch.

![notion_connexion.png](.readme_assets%2Fnotion_connexion.png)

### On Linear side
A [Linear account](https://linear.app/)  (same remark than for Notion, it works with the free plan).

A personal API key that you can create [here](https://linear.app/settings/api).

## Usage
### Configuration file
First of all, edit the file [configuration.properties](resources%2Fconfiguration.properties) by adding the values corresponding to your environment:
* `linear_api_key`: the personal API key you have created (cf. the section "Prerequisite");
* `notion_api_key`: the secret key of the notion integration you have created (cf. the section "Prerequisite");
* `team_key`: the key of the Linear project you want to analyze. In the ticket label, this is the first letters in uppercase before the '-' followed by the ticket number.
* `cycle_analysis_db_id`: (mandatory if you want to launch the cycle analysis, optional otherwise) the database on which the analysis document will be generated.

To get this database_id, on Notion click on the database view button and click on 'Copy link to view'.
![notion_copy_link_to_view.png](.readme_assets%2Fnotion_copy_link_to_view.png)
You will obtain a link on the following format:
https://www.notion.so/{domain-name}/{database_id}?v={view_id}&pvs=4. the number and letters chain in the database_id brackets is exactly what you are looking for.

* `bug_analysis_db_id`: (mandatory if you want to launch the bug analysis, optional otherwise) the database on which the analysis document will be generated.
* `ticket_analysis_db_id`: (mandatory if you want to launch the ticket analysis, optional otherwise) the database on which the analysis document will be generated.

<span style="color: #377B2A">**Note.**</span> You can visit [this Notion page](https://laromierre.notion.site/Linear-statistics-for-the-ABC-team-285e24e3521d4c6ba089350dc6d07ed7?pvs=4) to have an example of such databases, with the format of the document generated.

### Setup your python environment (python3)
First, create a python3 virtual environment
```commandline
virtualenv path/to/install/folder
source path/to/install/folder/bin/activate
```
Then, from the repository folder, execute the following command
```commandline
pip install -r requirements.txt
```
It installs dependencies used by the script.
Finally, set up the `PYTHONPATH` variable via the following command
```commandline
export PYTHONPATH=$PYTHONPATH:$PWD/src
```

### Launch the script
Again, from the repository folder, launch the script as follows:

```commandline
python src/main.py
```
With the following options:
```commandline
  -h, --help            show this help message and exit
  --properties-file-path PROPERTIES_FILE_PATH
  --max-nb-tickets-to-analyze MAX_NB_TICKETS_TO_ANALYZE
  -m {TICKET,BUG,CYCLE} [{TICKET,BUG,CYCLE} ...], --mode {TICKET,BUG,CYCLE} [{TICKET,BUG,CYCLE} ...]
                        list of modes, among 'TICKET', 'BUG' AND 'CYCLE'

```

Examples.
To display the help menu:
```commandline
python src/main.py -h
```
To launch a ticket analysis on the 23 last tickets:
```commandline
python src/main.py --max-nb-tickets-to-analyze=23 -m TICKET
```
To launch a bug analysis on the 12 last tickets, and a cycle analysis:
```commandline
python src/main.py --max-nb-tickets-to-analyze=12 -m BUG CYCLE
```
To launch a ticket, bug analysis on the 50 last tickets, and a cycle analysis, in specifying a specific properties file path (named 'another_conf_file.properties'):
```commandline
python src/main.py --properties-file-path=another_conf_file.properties --max-nb-tickets-to-analyze=50 -m TICKET BUG CYCLE
```
