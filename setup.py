import os
import subprocess
import requests
import zipfile

# Final dataset URLs
DATASETS = {
    "KITTI": "https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip",
    "NYU_Depth_Labeled": "http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat",
    "COCO": "http://images.cocodataset.org/zips/train2017.zip",
    "PhysioNet_EEG": "https://physionet.org/static/published-projects/eegmmidb/eeg-motor-movementimagery-dataset-1.0.0.zip"
}

# Function to install dependencies
def install_dependencies():
    print("📦 Installing dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# Function to create necessary directories
def create_directories():
    print("📂 Creating required directories...")
    directories = ["data/raw", "data/processed", "models", "modules", "utils", "experiments", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories set up successfully.")

# Function to download datasets
def download_dataset(name, url):
    save_path = os.path.join("data/raw", f"{name}.zip" if ".zip" in url else f"{name}.mat")
    if os.path.exists(save_path):
        print(f"✅ {name} dataset already exists. Skipping download.")
        return
    
    print(f"⬇️ Downloading {name} dataset...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    print(f"✅ {name} dataset downloaded.")

# Function to extract datasets
def extract_datasets():
    print("📂 Extracting datasets...")
    for name, url in DATASETS.items():
        file_path = os.path.join("data/raw", f"{name}.zip")
        if os.path.exists(file_path) and ".zip" in file_path:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall("data/raw")
            print(f"✅ Extracted {name} dataset.")

# Run all setup tasks
if __name__ == "__main__":
    install_dependencies()
    create_directories()
    for dataset, url in DATASETS.items():
        download_dataset(dataset, url)
    extract_datasets()
    print("🚀 Setup complete! You are ready to start developing BVT.")

