import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

tpd_df = pd.read_csv('data/viz.csv')


def visualize_token_distribution():
    # Mock data for token distribution
    token_counts = np.random.randint(50, 500, 100)
    plt.figure(figsize=(10, 6))
    plt.hist(token_counts, bins=30, color='skyblue', edgecolor='black')
    plt.title('Token Distribution')
    plt.xlabel('Number of Tokens')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

def visualize_token_pdfs_dist():
    # Set the width of each bar
    bar_width = 0.35

    x = np.arange(len(tpd_df['pdf_name']))
    plt.figure(figsize=(4,3))
    plt.bar(x - bar_width/2, tpd_df['pages'], width=bar_width, label='Pages')
    plt.bar(x + bar_width/2, tpd_df['tokens'], width=bar_width, label='Tokens')

    plt.xticks(x, tpd_df.index, rotation=90)

    plt.xlabel('PDF')
    plt.ylabel('Count')
    plt.title('Pages and Tokens Count for Each PDF')
    plt.legend()

    plt.tight_layout()
    st.pyplot(plt)


visualize_token_distribution()

st.header("Token Distribution per Document")
visualize_token_pdfs_dist()