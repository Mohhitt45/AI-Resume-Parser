from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def create_report(result):

    pdf = SimpleDocTemplate("Resume_Report.pdf")
    story = []

    story.append(Paragraph("<b>AI Resume Intelligence Report</b>", styles["Title"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    match_score = result.get("match_score", 0)
    story.append(Paragraph(f"Job Match Score : {match_score}%", styles["Heading2"]))

    if "resume_data" in result:

        parsed = result["resume_data"]
        info = parsed.get("basic_info", {})

        story.append(Paragraph(f"<br/>Name : {info.get('name','N/A')}", styles["Normal"]))
        story.append(Paragraph(f"Email : {info.get('email','N/A')}", styles["Normal"]))
        story.append(Paragraph(f"Phone : {info.get('phone','N/A')}", styles["Normal"]))

        ats = result.get("ats", {})
        story.append(
            Paragraph(
                f"ATS Score : {ats.get('ats_score',0)}%",
                styles["Heading2"]
            )
        )

        story.append(Paragraph("<br/><b>Matched Skills</b>", styles["Heading2"]))
        for skill in result.get("matched_skills", []):
            story.append(Paragraph(skill, styles["Normal"]))

        story.append(Paragraph("<br/><b>Missing Skills</b>", styles["Heading2"]))
        for skill in result.get("missing_skills", []):
            story.append(Paragraph(skill, styles["Normal"]))

        story.append(Paragraph("<br/><b>Extracted Skills</b>", styles["Heading2"]))
        for skill in parsed.get("skills", []):
            story.append(Paragraph(skill, styles["Normal"]))

    pdf.build(story)

    return "Resume_Report.pdf"
