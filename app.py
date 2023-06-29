from flask import Flask, render_template, request, jsonify, redirect, send_from_directory
import subprocess
import os
import json
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_code = request.form['product_code']
        
        print(product_code)
        # Call the scraper script
        subprocess.run(['python', 'scraper.py', product_code])
        # Call the analyzer script
        subprocess.run(['python', 'analyzer.py', product_code])
        return redirect('/results/' + product_code)
    return render_template('index.html')


@app.route('/results/<product_code>')
def results(product_code):
    opinions_file = f'./opinions/{product_code}.json'
    stats_file = f'./stats/{product_code}.json'
    plots_folder = './plots'
    
    if os.path.exists(opinions_file) and os.path.exists(stats_file):
        with open(opinions_file, 'r', encoding='utf-8') as f:
            opinions_data = json.load(f)
        with open(stats_file, 'r', encoding='utf-8') as f:
            stats_data = json.load(f)
        
        plots = []
        for filename in os.listdir(plots_folder):
            if filename.startswith(product_code) and filename.endswith('.png'):
                plots.append(filename)
        
        return render_template('results.html', product_code=product_code, opinions=opinions_data, stats=stats_data, plots=plots)
    else:
        return render_template('error.html', message='Results not found.')

@app.route('/images/<product_code>/<type>')
def images(product_code, type):
    imagefile = f'./plots/{product_code}_{type}.png'
    return send_from_directory('', imagefile)

if __name__ == '__main__':
    app.run()