from flask import Flask, render_template, send_from_directory, redirect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import time  

app = Flask(__name__)

def generate_random_points():
    num_points = 1000
    x_coords = np.random.randint(0, 1001, num_points)
    y_coords = np.random.randint(0, 1001, num_points)
    return pd.DataFrame({'x': x_coords, 'y': y_coords})

def generate_image():
    # Her istekte yeni bir görsel oluştur
    df = generate_random_points()

    fig, ax = plt.subplots()
    grid_size = 200
    num_colors = (1000 // grid_size) + 1
    colors = list(mcolors.TABLEAU_COLORS.values())[:num_colors]

    color_index = 0
    for i in range(0, 1000, grid_size):
        for j in range(0, 1000, grid_size):
            mask = (df['x'] >= i) & (df['x'] < i + grid_size) & (df['y'] >= j) & (df['y'] < j + grid_size)
            ax.scatter(df[mask]['x'], df[mask]['y'], color=colors[color_index % len(colors)])
            color_index += 1

    plt.title('Rastgele Koordinatların Görselleştirilmesi')
    plt.xlabel('X Koordinatları')
    plt.ylabel('Y Koordinatları')
    plt.grid(True)

    # Her seferinde farklı bir dosya adı oluştur
    image_filename = f'coordinates_visualization_{time.time()}.jpeg'
    image_path = os.path.join('static', image_filename)

    # Yeni resmi kaydet
    plt.savefig(image_path)
    plt.close()

    return image_filename

@app.route('/')
def index():
    image_filename = generate_image()
    return render_template('index.html', image_filename=image_filename)

@app.route('/generate')
def regenerate_image():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
