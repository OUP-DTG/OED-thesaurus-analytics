OED Thesaurus analytics
-----------------------

Collection of scripts for various kinds of analysis and report-generation
related to the Historical Thesaurus dataset.


## Main bash script: pipeline.sh

The usual entry point is the top-level bash script `thesaurus_analytics.sh`, which
orchestrates the sequential running of each step in the pipeline.
`thesaurus_analytics.sh` is really just a list of commands to run the top-level
python script `main.py`, with the appropriate command-line argument
(see below).

Any steps that are not to be run can be commented out in `thesaurus_analytics.sh`. 

An individual processing step can be run by copying a line from
`thesaurus_analytics.sh` and running it directly on the command-line.


## Set-up for running pipeline.sh from the command line

Activate the Python 3.13 virtual environment

Open the thesaurus_analytics.sh bash script in an editor, e.g. Vim:

     vim thesaurus_analytics.sh

Uncomment all the pipeline steps to be run.

Save and exit thesaurus_analytics.sh (`:wq` in Vim)

Run thesaurus_analytics.sh:

     ./thesaurus_analytics.sh

If any step crashes, raises an uncaught exception, or otherwise fails
to complete with a non-zero exit code, the pipeline as a whole will halt
at that point.


## Command-line format

Command-line processes should take the general form:

    python main.py [step]
