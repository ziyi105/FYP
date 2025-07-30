# 🧠🦾 Natural Language to Robot Actions — Modular System for Grounded Robotic Execution

This project explores how intelligent robots can understand and execute natural language instructions by combining the reasoning power of Large Language Models (LLMs) with spatial grounding capabilities. It features a modular pipeline that translates high-level commands like *"move the chair closer to the table"* into low-level executable steps and coordinates for robotic control.

The system integrates:

* An **LLM-based action planner** for breaking down instructions
* A **Vision-Language Model (VLM)** or custom **GPS module** for mapping language to coordinates

---

## 🧩 Project Structure

### Key Components:

* `Dataset Creation`: Automates dataset generation using RoboCasa layouts. Includes generation of image patches and spatial descriptions with LLMs.
* `GPS Demo`: Demonstrates the **Grid Proposal Selection (GPS)** method, an RPN-inspired technique that reformulates spatial grounding as a grid classification task to be processed by LLMs like GPT-4o.

---

## 🧪 Demo: Grid Proposal Selection (GPS)

The GPS method enables LLMs to predict spatial targets by overlaying a numbered grid on the scene image. Instead of relying on bounding box prediction (which many LLMs struggle with), the LLM selects a grid cell based on spatial language.

### To run the demo:

```bash
python GPS_demo/demo.py
```

The script will:

* Load a scene image with overlaid grid
* Prompt the LLM (e.g. GPT-4o) with a spatial instruction
* Return the predicted grid location

---

## 📦 Dataset Collection Pipeline

The dataset creation process is divided into **five modular steps**, allowing you to capture, mark, annotate, and preprocess visual data from the RoboCasa simulation environment.

### 🗂️ Folder: `dataset_creation/`

Contains all scripts required to collect and prepare your dataset.

---

### 🔹 Step 1: Capture Raw Scene Images

Use `get_camera_view.py` to capture top-down (bird’s-eye view) images of the environment.

```bash
python dataset_creation/get_camera_view.py
```

* Connects to the RoboCasa simulator to take screenshots of the kitchen scene.
* Saves the images (e.g., `scene_001.jpeg`) to a designated folder.

---

### 🔹 Step 2: Preprocess the Images

Run `image_preprocessing.py` to crop and compress the raw images.

```bash
python dataset_creation/image_preprocessing.py
```

* Standardizes the image size and quality.
* Output: cleaned images stored in a new folder, ready for annotation.

---

### 🔹 Step 3: Mark Desired Goal Locations

Use `annotation.py` to manually mark the desired final location (e.g., where a chair should be placed) by clicking on the scene image.

```bash
python dataset_creation/annotation.py
```

* Opens an interactive GUI for each image.
* Saves the coordinates and associated image paths into `annotations.json`.
* These locations will later guide the captioning process.

---

### 🔹 Step 4: Generate Descriptions using LLM

Use `generate_descriptions.py` to generate natural language descriptions of the marked positions with an LLM (e.g., GPT-4o).

```bash
python dataset_creation/generate_descriptions.py
```

* Uses the red cross overlay and sends the image to the LLM to describe the location (e.g., “next to the sink”).
* Accepts or edits generated captions manually.
* Appends output to `annotations.json`.

---

### 🔹 Step 5: Clean and Normalize Descriptions

Run `text_preprocessing.py` to clean and normalize the LLM-generated descriptions.

```bash
python dataset_creation/text_preprocessing.py
```

* Applies rules to standardize spatial phrases (e.g., lowercase text, remove redundant phrases).
* Ensures consistent inputs for downstream training or evaluation.

---

### 📁 Final Outputs

You will obtain:

* `processed_images/` — standardized cropped images
* `annotations.json` — contains:

  * Red cross coordinates (goal position)
  * Cleaned spatial descriptions
  * Associated scene image paths
    
---

## 📌 Highlights

* **Cross-domain innovation**: Adapted Region Proposal Networks from computer vision to language grounding.
* **Practical NLP-Vision integration**: Demonstrated how LLMs can reason over spatial data through engineered prompts.
* **Open-ended potential**: The modular pipeline allows plugging in future models and using different environments.

---

## 📎 Requirements

* Python 3.8+
* OpenAI API key for GPT-4o or any other LLM model
* RoboCasa simulator (for dataset generation)

---

## 🧠 Acknowledgement

This project was developed as part of the Final Year Project at the National University of Singapore, with support from the Institute for Infocomm Research (I²R), A\*STAR.

---
