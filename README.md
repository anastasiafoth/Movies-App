# 🎬 Movies Database App

A command-line application to manage your movie collection, featuring SQL database storage, OMDb API integration, and web interface generation.

## ✨ Features

- **Movie Management**
  - Add movies with details from OMDb API
  - Update movie ratings
  - Delete movies from your collection
  - View all movies with sorting options

- **Data Visualization**
  - Generate rating histograms
  - View movie statistics (average, median ratings)

- **Web Interface**
  - Generate a static website of your movie collection
  - Responsive design with movie posters
  - Clean, modern UI

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/anastasiafoth/Movies-App.git](https://github.com/anastasiafoth/Movies-App.git)
   cd movies-app
   
2. Install dependencies:
    ```bash
   pip install -r requirements.txt

3. Set up your environment:
- Create a .env file in the project root
- Add your OMDb API key:    
``` 
API_KEY=your_omdb_api_key_here
```

### Usage
Run the application:
```bash
python movies.py
```

Main Menu Options:

1. List all movies
2. Add a new movie
3. Delete a movie
4. Update movie rating
5. Show movie statistics
6. Get a random movie
7. Search for a movie
8. Sort movies by rating
9. Sort movies by year
10. Filter movies
11. Create rating histogram
12. Generate website


### 🛠️ Technologies Used
- Python 3
- SQLite
- SQLAlchemy
- OMDb API
- Matplotlib (for histograms)
- HTML/CSS (for web interface)

### 📁 Project Structure
```
Movies-App/
├── _static/                # Web assets
│   ├── index.html          # Generated website
│   ├── index_template.html # Website template
│   └── style.css           # Styling
├── .env                    # Environment variables
├── movies.py               # Main application
├── movie_storage_sql.py    # Database operations
├── movies_web_generator.py # Website generation
└── movies.db               # SQLite database
```


### 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

### 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.