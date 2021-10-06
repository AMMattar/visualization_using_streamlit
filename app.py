from os import name
import pandas as pd
import numpy as np
import streamlit as st
import random
import matplotlib.pyplot as plt
from streamlit.elements import image
from streamlit.proto.Image_pb2 import Image
from toml import load
from PIL import Image

st.title("Visualization ADS App")

d = st.text_input("enter the number of the ads")
if d:
    try:
        d = int(d)
    except:
        "number of entries should be numeric value only"
#N = st.slider("Number of entries in CSV file", min_value=1, max_value=10000)
N = st.text_input("enter the number of the entries in the CSV file")
if N:
    try:
        N = int(N)
    except:
        "number of entries should be numeric value only"

ads_selected = []
data = st.file_uploader("upload the CSV", type=['csv'])


image_files_ = st.file_uploader(
    "upload your Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True, key="1")

if data:
    dataset = pd.read_csv(data)
    numbers_of_rewards_1 = [0] * d
    numbers_of_rewards_0 = [0] * d
    total_reward = 0
    for n in range(0, N):
        ad = 0
        # Keep track of the maximum reward pulled from the distributions
        max_random = 0
        for i in range(0, d):
            random_beta = random.betavariate(
                numbers_of_rewards_1[i]+1, numbers_of_rewards_0[i]+1)
            if(random_beta > max_random):
                max_random = random_beta
                ad = i
        ads_selected.append(ad)
        reward = dataset.values[n, ad]
        if(reward == 1):
            numbers_of_rewards_1[ad] = numbers_of_rewards_1[ad]+1
        else:
            numbers_of_rewards_0[ad] = numbers_of_rewards_0[ad]+1
        total_reward = total_reward + 1

    to_sort_dict = {}
    assign = []
    for i in range(d):
        x = numbers_of_rewards_0[i] + numbers_of_rewards_1[i]
        assign.append(x)

    if len(image_files_) == d:
        fig, ax = plt.subplots()
        ax.hist(ads_selected)
        st.pyplot(fig)
        for i in range(d):
            to_sort_dict[assign[i]] = image_files_[i]

    sorted_dict = sorted(to_sort_dict.items(), reverse=True)

    for i in sorted_dict:
        show_file = st.empty()
        show_file.image(i[1])


else:
    st.write("please choose your csv")
