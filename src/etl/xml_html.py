#pylint: skip-file
#type: ignore

import os
import sys
from lxml import etree
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from abs_paths import processed_xml_output_default_folder
default_html_file = os.path.join(processed_xml_output_default_folder,"rockets.html")


def xml_to_html(xml_f, html_f):
    tree = etree.parse(xml_f)
    root = tree.getroot()

    html_content = "<html><head><title>Launch Vehicle List</title></head><body>\n"
    html_content += f"<h1>{root.tag} Overview</h1>\n"
    # table containing serial num, lv name and agency
    html_content += "<table border='1' cellpadding='5' cellspacing='0'>\n"
    html_content += "<tr><th>Serial Num</th><th>LV Name</th><th>Agency</th></tr>\n"

    for rocket in root.findall("Rocket"):
        snum   = rocket.get("snum") 
        name   = rocket.find("Name").text
        agency = rocket.find("Manufacturer").text
        html_content += f"<tr><td>{snum}</td><td>{name}</td><td>{agency}</td></tr>\n"
        
    html_content += "</table>\n</body></html>"

    os.makedirs(os.path.dirname(html_f), exist_ok=True)

    with open(html_f, "w") as f:
        f.write(html_content)
    print(f"HTML file generated: {html_f}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert rockets XML to HTML table.")
    parser.add_argument("--i", required=True, help="Input XML file")
    

    parser.add_argument(
        "--o",
        default=default_html_file,
        help="Output HTML file (default: data/processed/rockets.html)"
    )

    args = parser.parse_args()
    xml_to_html(args.i, args.o)