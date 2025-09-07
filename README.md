# n8n Search Engine

A semantic search engine for CSV data using sentence transformers and FAISS for fast similarity search.

## 🚀 Features

- **Semantic Search**: Uses sentence transformers to understand the meaning behind your queries
- **Fast Search**: FAISS indexing for lightning-fast similarity search
- **CLI Interface**: Command-line tool for quick searches
- **Web Interface**: Beautiful Streamlit web app with interactive features
- **Easy Setup**: Simple installation and setup process

## 📁 Project Structure

```
csv_search_engine/
│
├── data/
│   └── workflows.csv           # Your CSV data
│
├── embeddings/
│   ├── workflow_embeddings.npy # Generated embeddings
│   └── faiss_index.index      # FAISS search index
│
├── src/
│   ├── build_index.py         # Build embeddings and index
│   ├── search.py              # CLI search interface
│   └── app.py                 # Streamlit web app
│
├── requirements.txt
└── README.md
```

## 🛠️ Setup Instructions

### 1. Install Python Dependencies

First, create a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

Place your CSV file in the `data/` folder as `workflows.csv`. Make sure it has at least these columns:
- `workflow`: Name or identifier for each item
- `description`: Text description to search through

Example CSV format:
```csv
workflow,description
workflow1,Automates email notifications when new form submissions are received
workflow2,Scrapes product data from e-commerce websites daily
workflow3,Integrates Slack with project management tools
```

### 3. Build the Search Index

Navigate to the `src/` folder and run:

```bash
cd src
python build_index.py
```

This will:
- Load your CSV data
- Generate semantic embeddings for all descriptions
- Build a FAISS index for fast searching
- Save everything to the `embeddings/` folder

## 🔍 Usage

### Command Line Interface

For quick searches from the terminal:

```bash
cd src
python search.py
```

Then enter your search queries interactively. Examples:
- "email automation"
- "data scraping"
- "notifications"
- "file backup"

### Web Interface (Recommended)

For a beautiful web interface with more features:

```bash
cd src
streamlit run app.py
```

This will open a web browser with:
- Interactive search box
- Similarity scores
- Example queries
- Downloadable results
- Dataset statistics

## 🎯 Example Queries

Try searching for:
- **"email automation"** - finds workflows related to email processing
- **"data scraping"** - finds web scraping and data extraction workflows  
- **"notifications"** - finds alert and notification workflows
- **"file backup"** - finds backup and storage workflows
- **"social media"** - finds social media automation workflows

## 🔧 Customization

### Using Your Own Data

1. Replace `data/workflows.csv` with your own CSV file
2. Make sure it has `workflow` and `description` columns
3. Run `python build_index.py` to rebuild the index
4. Start searching!

### Adding More Columns

You can modify the scripts to search through additional columns:

1. In `build_index.py`, combine multiple columns:
```python
# Instead of just description:
text_to_embed = df['description'] + ' ' + df['tags'] + ' ' + df['category']
embeddings = model.encode(text_to_embed.tolist())
```

2. Update the display in `search.py` and `app.py` to show additional columns

### Changing the Model

You can use different sentence transformer models for better results:

```python
# In build_index.py, search.py, and app.py, replace:
model = SentenceTransformer('all-MiniLM-L6-v2')

# With a more powerful model (larger but better):
model = SentenceTransformer('all-mpnet-base-v2')
```

## 📈 Performance

- **Index Building**: ~1-2 seconds per 1000 rows
- **Search Speed**: <100ms for most queries
- **Memory Usage**: ~1-2MB per 1000 embedded descriptions

## 🚀 Deployment

### Local Network Access

To make the web app accessible on your local network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

### Cloud Deployment

You can deploy this to:
- **Streamlit Cloud**: Push to GitHub and connect your repository
- **Heroku**: Add a `Procfile` with `web: streamlit run src/app.py`
- **AWS/GCP**: Use container deployment with the included dependencies

## 🛟 Troubleshooting

### "Model not found" error
Make sure you have an internet connection when first running the scripts. The sentence transformer model will be downloaded automatically.

### "Index not found" error
Run `python build_index.py` first to generate the search index.

### Slow performance
- Try a smaller sentence transformer model
- Reduce the number of search results returned
- Consider using a smaller dataset for testing

### Memory issues
- Use `faiss-cpu` instead of `faiss-gpu` if you don't have a GPU
- Try processing your data in smaller batches

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this search engine!
