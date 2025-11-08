import random
import shutil
import os

def screen_resume(file_path, output_dir):
    """
    Simple placeholder screening logic.
    You can integrate LLM or keyword-based scoring here.
    """
    keywords = ["python", "sql", "azure", "aws", "ml", "data", "pipeline"]
    score = random.randint(40, 100)

    # Good or bad classification (mock)
    if score >= 70:
        dest_folder = os.path.join(output_dir, "good")
        label = "Good"
    else:
        dest_folder = os.path.join(output_dir, "bad")
        label = "Bad"

    os.makedirs(dest_folder, exist_ok=True)
    shutil.copy(file_path, dest_folder)
    return label, score
