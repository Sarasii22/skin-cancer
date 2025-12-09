from weasyprint import HTML
import os

def generate_pdf(result_dir, data):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial; padding: 40px; background: #f9f9f9; }}
            .header {{ background: #d32f2f; color: white; padding: 20px; text-align: center; border-radius: 10px; }}
            .result {{ font-size: 24px; margin: 20px 0; }}
            .high {{ color: red; font-weight: bold; }}
            .low {{ color: green; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ccc; padding: 12px; text-align: left; }}
            th {{ background: #eee; }}
            img {{ max-width: 400px; margin: 10px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="header"><h1>Skin Cancer Detection Report</h1></div>
        <div class="result">
            <strong>Result:</strong> 
            { '<span class="high">MALIGNANT (Skin Cancer Detected)</span>' if data['is_cancer'] else '<span class="low">BENIGN (No Cancer)</span>' }
        </div>
        <p><strong>Confidence:</strong> {data['confidence']}%</p>
        <p><strong>Risk Level:</strong> {data['risk']}</p>
        <p><strong>ABCD Score:</strong> {data['abcd_score']} (Higher = More Suspicious)</p>

        <h2>ABCD Rule Details</h2>
        <table>
            <tr><th>Feature</th><th>Score</th></tr>
            <tr><td>Asymmetry</td><td>{data['abcd']['A']}</td></tr>
            <tr><td>Border Irregularity</td><td>{data['abcd']['B']}</td></tr>
            <tr><td>Color Variation</td><td>{data['abcd']['C']}</td></tr>
            <tr><td>Diameter</td><td>{data['abcd']['D']}</td></tr>
            <tr><td><strong>Total Score</strong></td><td><strong>{data['abcd']['Total']}</strong></td></tr>
        </table>

        <h2>Images</h2>
        <img src="original.jpg" />
        <img src="highlighted.jpg" />
        <img src="mask.png" style="background: #000;" />
    </body>
    </html>
    """
    pdf_path = os.path.join(result_dir, "report.pdf")
    HTML(string=html, base_url=result_dir).write_pdf(pdf_path)
    return pdf_path