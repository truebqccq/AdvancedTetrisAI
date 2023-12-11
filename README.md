***All files mentioned are located in the tetris_gym_env subdirectory***
Due to the layout of the environment, we are not sure if everything will still work properly if we changed the structure of the directory.
All required files can be found in ./tetris_gym_env  

### Notebook Files
There are three training notebook files included, each trains the model slightly differently -- two are linear with different grid orientation, the other uses convolution neural network.  
To run these files, run each cell up to and including the one that loads previous training data. The cells after will perform the training and export the results. To view the result directly, skip past those cells and run the last two on the notebook, which will create a sample video that showcases the result. HTML versions of these files are also included.

Alternatively, the "demo.ipynb" file can be used to directly see the outputs of the training states. Simply put the training state file name into the second cell, and run all cells.


### Save States
There are various training data files included that can be used to visualize the agent's behavior. These include the final output for each training model, as well as samples of the state data throughout our training process.

### Replay Videos
There are seven total replay videos included. The full_send video showcases the agent with initial training. Three of them were used as a part of our final presentation. The other three contains the final result video for our training.  

### Source Files
The source files for the environment are located in the gym-tetris folder. The src folder contains the original author's model and training, as well as some of our miscellaneous files containing code we used throughout the project.

### Additional Notes:
Certain files have been excluded in the submission zip due to the size requirements. These include the raw scores from the training (used to create graphs) and the convolutional network model (needed to create the convolutional model). They can be obtained from our github page.
