
from json import loads
from pathlib import Path

from jinja2 import Template

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def html_to_pdf(html_content, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Convert HTML-like content to ReportLab elements
    elements = []
    for line in html_content.split('\n'):
        if line.strip().startswith('<h1>'):
            elements.append(Paragraph(line.strip()[4:-5], styles['Heading1']))
        elif line.strip().startswith('<p>'):
            elements.append(Paragraph(line.strip()[3:-4], styles['Normal']))
        else:
            elements.append(Paragraph(line.strip(), styles['Normal']))
    
    doc.build(elements)    


def handler(body):
    name = body["template"]
    file = Path.cwd() / Path(f"utils/pdf/templates/{name}")
    print(file)

    if not file.exists():
        return {"status": 400, "err": "TEMPLATE NOT AVAILABLE"}
    
    with file.open("r") as stream:
        patient = body["patient"]
        record = body["record"]

        template = Template(stream.read())
        rendered = template.render(
            name=patient["name"],
            lastname=patient["lastname"],
            created_at=record["created_at"],
            title=record["title"],
            history=record["history"],
            analysis=record["analysis"],
            diagnosis=record["diagnosis"],
            treatment=record["treatment"]
        )
        html_to_pdf(rendered, f"outputs/record-{record['id']}.pdf")
