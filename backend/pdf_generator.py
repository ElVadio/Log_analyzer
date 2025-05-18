from fpdf import FPDF
from datetime import datetime
import os
 
class PDFGenerator:
    def __init__(self, output_folder="generated_pdfs"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def create_driver_log(self, entries, filename="sample_driver_log.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Header
        pdf.set_xy(10, 10)
        pdf.cell(40, 10, "TIME (CT)")
        pdf.cell(40, 10, "CODE")
        pdf.cell(80, 10, "LOCATION")
        pdf.cell(30, 10, "ODOMETER (MI)", ln=True)

        y = 20

        # Add log entries with proper positioning
        for entry in entries:
            pdf.set_xy(10, y)
            pdf.cell(40, 10, entry['time_str'])
            pdf.set_xy(50, y)
            pdf.cell(40, 10, entry['status'])
            pdf.set_xy(90, y)
            pdf.cell(80, 10, entry['location'])
            pdf.set_xy(170, y)
            pdf.cell(30, 10, str(entry['odometer']), ln=True)
            y += 10

        output_path = os.path.join(self.output_folder, filename)
        pdf.output(output_path)
        print(f"PDF generated: {output_path}")

    @staticmethod
    def generate_sample_entries():
        """
        Generate a few sample entries for testing.
        """
        return [
            {
                "time_str": "Mar 05, 08:20:54 am",
                "status": "Sleeper",
                "location": "14mi S from Mount Pleasant, IA",
                "odometer": 2760
            },
            {
                "time_str": "Mar 05, 06:28:20 am",
                "status": "On Duty",
                "location": "14mi S from Mount Pleasant, IA",
                "odometer": 2760
            },
            {
                "time_str": "Mar 05, 06:44:15 am",
                "status": "Driving",
                "location": "14mi S from Mount Pleasant, IA",
                "odometer": 2775
            },
            {
                "time_str": "Mar 05, 07:50:00 am",
                "status": "On Duty",
                "location": "5mi NE from Des Moines, IA",
                "odometer": 2795
            },
            {
                "time_str": "Mar 05, 08:10:00 am",
                "status": "Sleeper",
                "location": "Des Moines, IA",
                "odometer": 2800
            }
        ]

if __name__ == "__main__":
    generator = PDFGenerator()
    entries = generator.generate_sample_entries()
    generator.create_driver_log(entries)
