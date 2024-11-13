# Variational Gaussian Mixture Model (VGM) Data Transformation

This project implements a scalable and production-ready version of the Variational Gaussian Mixture Model (VGM), designed to efficiently process large datasets (up to 1 billion records). The goal is to transform and inverse-transform data using VGM while ensuring the code is optimized for speed, scalability, and correctness.

## Table of Contents
- [Overview](#overview)
- [API](#api)
- [Configuration](#configuration)
- [Model](#model)
- [Services](#services)
- [Utils](#utils)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
    - [Data Transformation](#data-transformation)
    - [Inverse Transformation](#inverse-transformation)
- [Requirements](#requirements)
    - [Step 1: Install Dependencies](#step-1-install-dependencies)
    - [Step 2: Run the Application](#step-2-run-the-application)
- [Inference API Requests](#inference-api-requests)
    - [Transform Request](#transform-request)
    - [Inverse Transform Request](#inverse-transform-request)
- [Docker Setup with Docker Compose](#docker-setup-with-docker-compose)
- [Folder Structure](#folder-structure)

---

## Overview

This project implements a scalable, production-ready solution to perform data transformations using a Variational Gaussian Mixture Model (VGM). The system processes large datasets by downloading them from a specified source, applying transformations, and saving the transformed data. It is built to handle up to 1 billion records efficiently using optimized techniques such as parallel data processing.

---

## API

The FastAPI application defines two main endpoints:

1. **Data Transformation Endpoint**: 
   - Downloads data from a Google Drive link, processes it in chunks, and saves the transformed results.
   
2. **Inverse Transformation Endpoint**: 
   - Takes transformed data and reverts it to its original form.

Both endpoints use Pydantic models for request validation and include error handling to return appropriate HTTP status codes.

---

## Configuration

The `config.py` file contains the configuration class that manages various application settings, such as:
- **Download directory**
- **Chunk size**
- **Maximum retries**
- **Timeout values**

These settings are loaded either from environment variables or default to predefined values, providing flexibility in managing runtime parameters.

---

## Model

In the `transformer.py` file, the `DataTransformer` class prepares data for training by:
- Converting categorical, continuous, and mixed-type data into a standardized format.
- Using Bayesian Gaussian Mixture Models (BGM) for continuous and mixed columns, which helps capture different patterns in the data.
- Applying techniques like one-hot encoding for categorical data and custom transformations for continuous/mixed data.

The class also includes an inverse transformation method to revert the model’s output back to its original form.

---

## Services

The `model_service.py` file handles the core functionality of data transformation and inverse transformation. It:
- Downloads the data.
- Processes it in parallel chunks.
- Saves the results to disk.
- Manages retries and error handling during data processing.

The service utilizes the transformer to apply and reverse the transformations.

---

## Utils

The `drive_handler.py` file provides a handler for downloading data from Google Drive. It:
- Uses a provided Google Drive link to fetch the file.
- Handles retries in case of failure.
- Saves the downloaded file to the configured directory, ensuring smooth access and processing.

---

## Key Features

- Scalable data processing with parallel execution.
- VGM model transformation and inverse transformation.
- Production-ready architecture with error handling and logging.
- Performance optimizations for handling large datasets.

---

## Technologies Used

- **Python**: Pandas, Scikit-learn, FastAPI, Numpy
- **Multi-threading**: `concurrent.futures`
- **Docker**: For containerization

---

## Usage

This project is designed to process and transform large datasets using the VGM model. It offers two main functionalities:

### Data Transformation

To transform a dataset:
1. Provide a link to the source data file (e.g., from Google Drive).
2. The data will be processed in chunks, transformed, and saved in an output file.

### Inverse Transformation

Once the data is transformed, the inverse transformation can be applied to revert to the original data format.

---

## Requirements

Before running the project, install the required dependencies.

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

Start the server to serve the model via FastAPI using `uvicorn`.

```bash
uvicorn app.api.routes:app --reload
```

This will launch a local development server on `http://localhost:8000`.

---

## Inference API Requests

There are two main requests available for inference:

### Transform Request

This API takes a Google Drive link to download the dataset, processes it using VGM, and returns the transformed data.

**Curl Command**:

```bash
curl -X POST http://localhost:8000/api/v1/transform \
     -H "Content-Type: application/json" \
     -d '{"drive_link": "https://drive.google.com/file/d/1BMZPas2dQI9R4hvUQ6v6Sxdgjpoak_rj/view?usp=drive_link"}'
```

### Inverse Transform Request

This API allows you to inverse the transformed data back to its original form.

**Curl Command**:

```bash
curl -X POST "http://localhost:8000/api/v1/inverse_transform" \
     -H "Content-Type: application/json" \
     -d "{\"transformed_file_path\": \"insert/your/path/here.csv\"}"
```

---

## Docker Setup with Docker Compose

To run the application using Docker Compose, follow these steps:

### Step 1: Build and Run the Application with Docker Compose

```bash
docker-compose up --build
```

This command will build the image (if not already built) and start the container.

---

## Folder Structure

The project is organized as follows:

```
app/
├── api/
│   └── routes.py               # FastAPI application routes
├── config/
│   └── config.py               # Configuration management
├── models/
│   └── transformer.py          # Data transformation model
├── services/
│   └── model_service.py        # Core transformation service
├── utils/
│   └── drive_handler.py        # Google Drive file handler
├── .gitignore                  # Git ignore file
├── Dockerfile                  # Dockerfile for containerization
├── README.md                   # Project documentation
├── docker-compose.yml          # Docker Compose configuration
└── requirements.txt            # Python dependencies
```

---

This README provides a comprehensive overview of the project structure, features, usage, and setup instructions.
