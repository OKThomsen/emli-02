import subprocess

def take_tempphoto():
    try:
        # Execute the command to capture a photo
        subprocess.run(["rpicam-still", "-t", "0.01", "-o", "./tempphotos/picture2.jpg"], check=True)
        print("Photo captured successfully.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

if __name__ == "__main__":
    take_tempphoto()
