#!/usr/bin/env bash

#=============================================================================
#
# theasurus_analytics
# =======================
#
# Batch process manager to run steps for various Historical Thesaurus analytics.
#
# Usage
# -----
#
# 1. cd to the directory containing this file.
#
# 2. Comment out any processes in this file that you do not want to run.
#
# 3. Run this file:
#    > ./thesaurus_analytics.sh
#
#=============================================================================


#----------------------------------------------------------------------------
# Bash settings
#----------------------------------------------------------------------------

# When a command fails, bash exits instead of continuing with the rest
#  of the script
set -o errexit
# Make the script fail, when accessing an unset variable.
set -o nounset
# Ensure that a pipeline command is treated as failed, even if one
#  command in the pipeline fails
set -o pipefail

# Enable debug mode, by doing "TRACE=1 ..sh"
if [[ -n "${TRACE-}" ]]; then
    set -o xtrace
fi

# Display help message if user does "./computing_spreadsheet.sh -h" or
#  "./computing_spreadsheet.sh --help"
ARG1=${1:-foo}
if [[ "$ARG1" =~ ^-*h(elp)?$ ]]; then
    echo '
thesaurus_analytics.sh
----------------------

Usage:
    ./thesaurus_analytics.sh

Batch process manager to run steps for various Historical Thesaurus analytics.
'
    exit
fi

# cd to the directory containing this file
cd "$(dirname "$0")"


# ------------------------------------------------
# Computing senses:
# Generate a CSV file listing computing senses
#  and their categorization in the Historical Thesaurus
# ------------------------------------------------

python main.py computing_senses_compile_senses
python main.py computing_senses_replace_nodes_with_breadcrumbs



# -----------------------------------------------
# Partials:
# Aggregate JSON records for approved classifications, etc.,
# into human-friendly CSV file
# -----------------------------------------------

#python main.py partials_list_attnthes_comments
#python main.py partials_list_partial
#python main.py partials_list_approved
#python main.py partials_list_incorrect
#python main.py partials_subcategorize_partials
