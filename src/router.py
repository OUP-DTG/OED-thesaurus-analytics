"""
Router to run functions in the thesaurus-analytics pipeline.
"""

from collections.abc import Callable

from src import steps


def run_process(process_name: str, **kwargs) -> None:
    """
    Locate the function corresponding to the process_name argument, and pass
    it to the functionrunner along with any arguments.

    Parameters
    ----------
        process_name : str
            The command-line process-name.

        kwargs : dict
            Any other arguments derived from command-line args.
    """
    func = _get_function(process_name.lower().replace("_", "").strip())
    func(**kwargs)


def _get_function(process_name: str) -> Callable:
    """
    Locate the function corresponding to the process_name argument.

    Parameters
    ----------
        process_name : str
            The command-line process-name.

    Returns
    -------
        callable
            The function to be run.
    """
    match process_name:
        case "computingsensescompilesenses":
            fnc = steps.computing_senses.list_senses
        case "computingsensesreplacenodeswithbreadcrumbs":
            fnc = steps.computing_senses.replace_nodes

        case "partialslistattnthescomments":
            fnc = steps.partials.list_attnthes_comments
        case "partialslistapproved":
            fnc = steps.partials.approved_to_csv
        case "partialslistpartial":
            fnc = steps.partials.partials_to_csv
        case "partialslistincorrect":
            fnc = steps.partials.incorrect_to_csv
        case "partialssubcategorizepartials":
            fnc = steps.partials.subcategorize_partials
        case "listlongcategoryheaders":
            fnc = steps.long_category_headers.list_long_category_headers
        case _:
            raise ValueError(f"{process_name} is not a valid process name")
    return fnc
