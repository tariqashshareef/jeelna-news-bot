"""Builds a weekly report of summarized article themes."""

def make_report(sections):
    """
    Creates a markdown report with one section per theme.
    
    Args:
        sections: A list of dicts with "theme" and "summary" keys.

    Returns:
        A markdown report as a string.
    """

    lines = []
        
    for section in sections:
        lines.append(f"## {section['theme']}")
        lines.append(section["summary"])
        lines.append("")

    return "\n".join(lines)