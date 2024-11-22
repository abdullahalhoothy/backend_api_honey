import pandas as pd
import re
import requests
from pathlib import Path
from fastai.vision.all import *
from collections import Counter
from urllib.parse import urlparse, parse_qs
import albumentations as A
import cv2
import os
from skimage import io
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from fastai.callback.progress import ShowGraphCallback


# Function to sanitize filenames by removing or replacing invalid characters
def sanitize_filename(name):
    """Sanitize the filename by removing or replacing invalid characters and sequences."""
    name = re.sub(r'[\\/*?:"<>|,\s+\0]', "", name)  # Remove problematic characters including null byte
    # name = re.sub(r'\s+', '_', name)  # Replace spaces with underscores to prevent issues
    return name[:150]


def is_valid_url(url):
    """Check if the URL is valid, assuming URLs should be non-empty strings."""
    if not isinstance(url, str):
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_drive_direct_link(gdrive_url):
    """Convert a Google Drive sharing URL to a direct download link."""
    parsed_url = urlparse(gdrive_url)
    file_id = parse_qs(parsed_url.query).get('id')
    if file_id:
        return f"https://drive.google.com/uc?export=download&id={file_id[0]}"
    return None

def download_images(urls, dest):
    """Download images from a list of URLs to a specified directory, handling possible errors."""
    dest.mkdir(parents=True, exist_ok=True)
    j=0
    for i, url in enumerate(urls):
        print(url)
        if not is_valid_url(url):
            print(f"Skipping invalid URL: {url}")
            continue

        try:
            j = j+1
            print(dest)
            downloadImage(url, str(dest)+'/', j)
        except requests.RequestException as e:
            print(f"Failed to download {url} due to {e}")



def downloadImage(url, path, counter=1):
    # Send a GET request to the URL
    toks = url.split("/")
    file_id = toks[5]
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'PHPSESSID=ABCDEFG',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8',
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    print(response.status_code)
    if response.status_code == 200:
        # Open a file in binary-write mode
        with open(path+str(counter)+".png", "wb") as file:
            file.write(response.content)
            print("Image downloaded successfully!")




# Function to apply the augmentation to an image and save it
def augment_and_save(image_path, save_path, count):
    image = io.imread(image_path)
    image = transform(image=image)['image']
    save_file_path = f"{save_path}/{count}.png"
    io.imsave(save_file_path, image)




#Without Split
def prepare_data(path):
    files = get_image_files(path)
    labels = [parent_label(p) for p in files]
    label_count = Counter(labels)

    # Set up data block
    coffee_block = DataBlock(
        blocks=(ImageBlock, CategoryBlock), 
        get_items=get_image_files, 
        splitter=FuncSplitter(lambda idx: False),  # Always return False to keep all in the training set
        get_y=parent_label,
        item_tfms=Resize(460),
        batch_tfms=[*aug_transforms(size=224, min_scale=0.75), Normalize.from_stats(*imagenet_stats)]
    )

    dls = coffee_block.dataloaders(path, path=path)

    # Displaying label counts to understand the distribution
    print("Training labels:", Counter([parent_label(o) for o in dls.train.items]))
    
    # Check for singletons and conditionally add transforms
    if any(label_count[label] == 1 for label in label_count):
        additional_tfms = aug_transforms(mult=2, do_flip=True, flip_vert=True, max_rotate=30.0, min_zoom=1.0, max_zoom=2.0, max_lighting=0.2, max_warp=0.2)
        # Extend the training set's after_batch pipeline with additional transformations
        dls.train.after_batch = Pipeline([*dls.train.after_batch.fs, *additional_tfms])

    return dls



#Train Valid Split
def prepare_data(path):
    # Get all image files
    files = get_image_files(path)
    # Obtain labels from file paths
    labels = [parent_label(f) for f in files]
    
    # Perform stratified split
    train_files, valid_files = train_test_split(
        files, test_size=0.5, stratify=labels, random_state=42)
    
    # Create a mapping from file to index
    file2idx = {f: i for i, f in enumerate(files)}
    train_idxs = [file2idx[f] for f in train_files]
    valid_idxs = [file2idx[f] for f in valid_files]
    
    # Define the DataBlock with a custom splitter
    dblock = DataBlock(
        blocks=(ImageBlock, CategoryBlock),
        get_items=lambda x: files,  # Use the predefined list of files
        get_y=parent_label,
        splitter=IndexSplitter(valid_idxs),  # Use IndexSplitter with valid indices
        item_tfms=Resize(460),
        batch_tfms=aug_transforms(size=224, min_scale=0.75)
    )
    
    # Create the DataLoaders
    dls = dblock.dataloaders(path)
    return dls



def train_model(dls):
    # Initialize the learner with ResNet-101
    learn = vision_learner(dls, resnet34, metrics=accuracy, pretrained=True)
    
    # Step 1: Precompute activations and enable data augmentation
    learn.freeze()
    learn.fit_one_cycle(1, lr_max=1e-3)  # Pre-train the head with a low learning rate

    # Step 2: Finding the optimal learning rate
    lr_find_result = learn.lr_find()
    lr_suggestion = lr_find_result.valley  # Using valley to get the suggestion
    print(f"Suggested learning rate: {lr_suggestion:.2e}")

    # Step 3: Train only the last layer group with the found learning rate
    learn.fit_one_cycle(2, lr_max=lr_suggestion)

    # Step 4: Unfreeze the model and set differential learning rates
    learn.unfreeze()
    base_lr = lr_suggestion / 10
    learn.fit_one_cycle(10, lr_max=slice(base_lr/100, base_lr))

    # Step 5: Use fine-grained learning rate adjustments with cycle_mult
    learn.fit_one_cycle(8, lr_max=slice(base_lr/100, base_lr))

    return learn




def train_model(dls):
    # Initialize the learner with ResNet-34
    learn = vision_learner(dls, resnet34, metrics=accuracy, pretrained=True)

    # Step 1: Precompute activations and enable data augmentation
    learn.freeze()
    learn.fit_one_cycle(1, lr_max=1e-3)  # Pre-train the head with a low learning rate

    # Step 2: Finding the optimal learning rate
    lr_find_result = learn.lr_find()
    lr_suggestion = lr_find_result.valley  # Using valley to get the suggestion
    print(f"Suggested learning rate: {lr_suggestion:.2e}")

    # Step 3: Train only the last layer group with found learning rate
    learn.fit_one_cycle(2, lr_max=lr_suggestion)

    # Step 4: Unfreeze the model and set differential learning rates
    learn.unfreeze()
    base_lr = lr_suggestion / 10
    learn.fit_one_cycle(10, lr_max=slice(base_lr/100, base_lr), cbs=[ShowGraphCallback()])

    # Step 5: Use fine-grained learning rate adjustments with cycle_mult
    learn.fit_one_cycle(8, lr_max=slice(base_lr/100, base_lr), cbs=[ShowGraphCallback()])

    return learn




# Train the model on the dataloaders set up with all data in the training set
dlss = prepare_data(Path('D:/CV/Coffee Brand Prediction/Images'))
learn = train_model(dlss)
learn = train_model(dlss)
# Define an augmentation pipeline
transform = A.Compose([
    A.HorizontalFlip(p=0.5),              # Apply horizontal flip to 50% of images
    A.RandomBrightnessContrast(p=0.2),    # Apply random brightness or contrast
    A.Rotate(limit=40, p=0.5),            # Rotate by angle between -40 and +40 degrees 50% prob.
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.5),
    A.Resize(256, 256)                    # Resize images to 256x256
])



# Use the modified prepare_data function
path = Path('D:/CV/Coffee Brand Prediction/Images')
dlss = prepare_data(path)
print(dlss)
dlss.show_batch()




# Usage
dlss = prepare_data(Path('D:/CV/Coffee Brand Prediction/Images'))
print(dlss)
dlss.show_batch()


# Path to the dataset
dataset_dir = 'Images'

# Augment images in each subdirectory and continue the image numbering
for subdir, dirs, files in os.walk(dataset_dir):
    # Prepare the directory to save the augmented images
    save_dir = subdir
    
    # Calculate the starting count based on existing files that end with .png (to prevent reading other files)
    existing_images = [int(f.split('.')[0]) for f in files if f.endswith('.png')]
    if existing_images:  # Ensure there are existing png images
        start_count = max(existing_images) + 1
    else:
        start_count = 1
    
    # Augment and save each image
    for file in files:
        if file.endswith('.png'):  # Process only PNG images to avoid duplicates
            image_path = os.path.join(subdir, file)
            augment_and_save(image_path, save_dir, start_count)
            start_count += 1

path = Path('D:/CV/Coffee Brand Prediction/Images')
# Verify folder structure and contents
for label_dir in path.iterdir():
    if label_dir.is_dir():
        images = list(label_dir.glob('*'))
        if not images:
            print(f"No images found in {label_dir.name}")
        else:
            print(f"{label_dir.name}: {len(images)} images")

# Path to the Excel file containing product data
excel_path = 'D:/CV/Coffee Brand Prediction/productssmal.xlsx'
product_df = pd.read_excel(excel_path)
product_df.head()


# Example usage
path = Path('C:/Users/MuhammadAhmad/Downloads/Coffee Brand Prediction/Images')
product_df = pd.read_excel('C:/Users/MuhammadAhmad/Downloads/Coffee Brand Prediction/productssmal.xlsx')
for _, row in product_df.iterrows():
    product_name = row['Product Name']  # assuming sanitize_filename function is defined elsewhere
    img_urls = [row['Image 1 Link'], row['Image 2 Link']]
    print(img_urls)
    dest = path / sanitize_filename(str(product_name))
    download_images(img_urls, dest)


# Save the trained model for later use or inference
learn.export('Resnet34_Full_trained_model.pkl')

# Example usage
path = Path('C:/Users/MuhammadAhmad/Downloads/Coffee Brand Prediction/Images')
product_df = pd.read_excel('C:/Users/MuhammadAhmad/Downloads/Coffee Brand Prediction/productssmal.xlsx')
for _, row in product_df.iterrows():
    product_name = row['Product Name']  # assuming sanitize_filename function is defined elsewhere
    img_urls = [row['Image 1 Link'], row['Image 2 Link']]
    print(img_urls)
    dest = path / sanitize_filename(str(product_name))
    download_images(img_urls, dest)


# # Load the trained model and define a function for performing inference on new images
# learn_inf = load_learner('trained_model.pkl')

# def predict_image(image_path):
#     img = PILImage.create(image_path)
#     pred, pred_idx, probs = learn_inf.predict(img)
#     return pred, probs[pred_idx]

# # Example of inference on a new image
# predict_image('path_to_test_image.jpg')