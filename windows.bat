SET mypath=%cd%
CALL "%cd%\.venv\Scripts\activate"
python download_files.py
python merge_files.py