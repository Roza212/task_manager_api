import subprocess
from PIL import Image, ImageDraw, ImageFont

def generate_screenshot():
    print("Running pytest...")
    pytest_out = subprocess.run(["pytest", "tests/", "-v"], capture_output=True, text=True).stdout
    
    print("Running populate...")
    subprocess.run(["python", "populate.py"])
    
    print("Running validate_db.py...")
    val_out = subprocess.run(["python", "validate_db.py"], capture_output=True, text=True).stdout

    # We want to capture the terminal command and output for the screenshot
    text_content = f"PS E:\\Antigravity\\task_manager_api> pytest tests/ -v\n{pytest_out}\n\nPS E:\\Antigravity\\task_manager_api> python validate_db.py\n{val_out}"

    lines = text_content.split('\n')
    # Focus on the end of pytest and the validate_db output
    lines = lines[-40:]

    # Create image
    img_width = 900
    img_height = 650
    img = Image.new('RGB', (img_width, img_height), color=(12, 12, 12))
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("consola.ttf", 15)
    except:
        font = ImageFont.load_default()

    y = 20
    for line in lines:
        if "FAIL" in line:
            color = (255, 80, 80)
        elif "PASS" in line or "passed" in line.lower():
            color = (80, 255, 80)
        elif "PS E:\\" in line:
            color = (255, 255, 100)
        else:
            color = (220, 220, 220)
            
        d.text((20, y), line, fill=color, font=font)
        y += 15

    img.save('docs/db_validation_results.png')
    print("Saved docs/db_validation_results.png")

if __name__ == "__main__":
    generate_screenshot()
