from bs4 import BeautifulSoup
import logging
import textwrap


from bs4 import NavigableString

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def process_text_node(text):
    """
    This function is called for each text node in the HTML.
    Modify this function to perform the desired operation on the text.

    Args:
        text (str): The text content of the node.
    """
    # Replace this with your desired processing logic
    processed_text = text.strip()  # Example: Remove leading/trailing whitespace
    if processed_text:
        result = processed_text[::-1].upper()
    else:
        result = processed_text
    return result


def copy_html_nodes(html_string):
    """
    Parses an HTML string and recursively copies its nodes,
    calling process_text_node() for any plain text nodes.

    Args:
        html_string (str): The HTML string to process.

    Returns:
        str: A string representing the copied HTML.  Crucially, the text
             content of the returned HTML will have been processed by
             process_text_node.
    """
    soup = BeautifulSoup(textwrap.dedent(html_string), "html.parser")
    new_soup = BeautifulSoup(
        "", "html.parser"
    )  # Create a new empty soup to hold the copied and modified structure

    def _copy_node(node, parent):
        """
        Recursive helper function to copy and process nodes.

        Args:
            node (bs4.element.Tag or bs4.element.NavigableString): The current node to process.
            parent (bs4.element.Tag): The parent node in the *new* tree to which the copy should be added.
        """
        if isinstance(node, NavigableString):
            # It's a text node, so process it
            processed_text = process_text_node(node)
            if processed_text:
                new_node = NavigableString(processed_text)
                parent.append(new_node)
        else:
            # It's an element (tag), so create a copy of the tag
            new_node = new_soup.new_tag(node.name)
            # Copy attributes
            for attr, value in node.attrs.items():
                new_node[attr] = value
            parent.append(new_node)

            # Recursively copy children
            for child in node.contents:
                _copy_node(child, new_node)

    # Start the copying process from the root of the original soup
    for child in soup.contents:
        _copy_node(child, new_soup)

    return str(new_soup.prettify())  # Return the modified HTML as a string


def main():
    """
    Main function to demonstrate the usage of copy_html_nodes().
    """
    html_content = """
    <html>
        <head>
            <title>My Document</title>
            <style>
              /* This is some CSS */
              body {
                color: blue;
              }
            </style>
        </head>
        <body>
            <h1>Welcome</h1>
            <p>This is a <b>paragraph</b> with <i>mixed</i> <strong>formatting</strong>.</p>
            <p>Here is some text with no formatting.</p>
            <div>
                <p>Another paragraph, inside a div.</p>
                <ul>
                  <li>List item 1</li>
                  <li>List item 2</li>
                </ul>
            </div>
            <script>
               // This is javascript
               var x = 10;
            </script>
        </body>
    </html>
    """

    processed_html = copy_html_nodes(html_content)
    print(processed_html)


if __name__ == "__main__":
    main()
