from presentation.color import Color
from presentation.tag import Tag


def print_header(in_file, from_file, testing):
    """
    print_header()
        Print a couple of introduction lines

    Args:
        testing:
        from_file:
        in_file:
    """

    if not from_file:
        header_msg = "{0} Checking for duplicate files in {1} {2} {3}".format(
            Tag.info, Color.bold_green, in_file, Color.end)
    else:
        header_msg = "{0} Checking for duplicate files from {1} {2} {3} in {4} {5} {6}".format(
            Tag.info, Color.bold_green, from_file, Color.end, Color.bold_green, in_file, Color.end)

    if not testing:
        print(header_msg)
    else:
        print("{0} [TEST] {1}".format(header_msg, Color.end))


def print_duplicated_msg(item, match_ratio, times):
    """
    duplicated(in_file, from_file)
        Prints duplicated item found.

    Args:
        times:
        item:
        match_ratio:
    """
    str_item = "{0}{1}{2}".format(Color.bold_green, item, Color.end)

    if match_ratio == 100:
        str_match = "found. {0}{1}%{2} match".format(
            Color.bold_red, match_ratio, Color.end)
    else:
        str_match = "possible match. {0}{1}%{2} match".format(
            Color.bold_yellow, match_ratio, Color.end)

    print("* {0} {1} ({2} times)".format(str_item, str_match, times))
