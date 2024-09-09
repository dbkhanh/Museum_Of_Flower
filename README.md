# MuseumOfFlower

## Overview

Welcome to the Museum of Flowers project! This repository contains a web application designed to showcase a curated collection of flowers by providing users with an interactive experience. 

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:
`git clone https://github.com/dbkhanh/Museum_Of_Flower.git
cd Museum_Of_Flower
`
2. Set up env
```python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Config Database - make sure to update database connection settings

4. Run the application
```
uvicorn backend.main:app --reload
```

and application will run on: http://127.0.0.1:5000

