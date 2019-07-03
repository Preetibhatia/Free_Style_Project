# Free_Style_Project
Amazon Scraper for monitoring and tracking product price 

Create and activate a new Anaconda virtual environment:
conda create -n amazon-env python=3.7 # (first time only)
conda activate amazon-env


From within the virtual environment, install the required packages
third party packages: pandas, numpy, matplotlib,lxml,requests
pip install pandas
pip install numpy
pip install matplotlib
#alternatively can use requirement.txt file
pip install pytest 
#(only if you'll be writing tests)

create directory app (first-time)
create directory data(first-time)


Create .env file and save your desired sender email id and password
Ensure .env is included in .gitgnore file



From within the virtual environment, demonstrate your ability to run the Python script from the command-line:
python amazon.py