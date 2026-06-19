from jinja2 import Environment, FileSystemLoader


def generate_html_report(
    global_score,
    completeness,
    uniqueness,
    email_validity,
    profile,
    output_path="reports/report.html"
):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")

    html_content = template.render(
        global_score=global_score,
        completeness=completeness,
        uniqueness=uniqueness,
        email_validity=email_validity,
        profile=profile
    )

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_content)