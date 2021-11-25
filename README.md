# Literature Image Scraper (v1.0.0)

Developed and maintained by [Tianjun Liu](irene.liutj@gmail.com).

------

Python scripts to 

1. scrape images from PDF files;
2. detect if those images contain certain insect;
3. export file list and image information for references, including the object detection results.

The current version `v1.0.0` only includes detection model for earwigs. Further insect groups will be developed upon requests.

Most operations in this documentation are executed in `Bash` Command-Line-Interface (Terminal, cmd, etc.).

## 1. Dependencies

To use `ImageAI` for object detection, some packages in certain versions are used. It is recommended to execute this application in another [virtual environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

### 1.1. Linux & MacOS

#### 1.1.1. Installation

Install Anaconda [for Linux](https://docs.anaconda.com/anaconda/install/linux/);  [for MacOS.](https://docs.anaconda.com/anaconda/install/mac-os/)

#### 1.1.2. Setup an environment

Create a new environment:

```bash
conda create --name myenv python=3.7.6
```

- Replace `myenv` with the environment name, e.g. `imageai`, `scraper`, etc.


Activate this environment:

```bash
conda activate myenv
```

Install dependencies for object detection:

```bash
pip install numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 keras-resnet==0.2.0
pip install tensorflow==2.4.0 keras==2.4.3 opencv-python imageai
```

Install dependencies for PDF scraping:

```
pip install PyMuPDF Pillow
```

### 1.2. Windows

#### 1.2.1. Installations

Install [Git Bash](https://git-scm.com/download/win).

Install Anaconda [for Windows](https://docs.anaconda.com/anaconda/install/windows/).

Open `Git Bash` and type in the command `~/anaconda3/Scripts/conda.exe init bash` to activate both `Python` and `Conda`.

#### 1.2.2. Setup an environment

See 1.1.2.



## 2. Installation

Clone the repository to your local directory:

```bash
cd ~/<your_path>
git clone git@github.com:tianjunl/literature_image_scraper.git
```

- Replace `<your_path>` with the your local repository path.



## 3. Literature Scraping

### 3.1. Input files

Please copy your PDF files to `literature_image_scraper/data/pdf`. There are three test files in this folder. Please replace them with your own files.

### 3.2. Execute the program

Change to the working directory:

```bash
cd ~/<your_path>/literature_image_scraper
```

Run the main program `scraper.py`:

```bash
python scraper.py
```

### 3.3. User parameters

You will be asked to enter some input info. 

1. `max_page` The default value is `20`.

   If you have scanned books in the pdf folder, each page will be analyzed and saved, and this will take long. To save time, skip these pdf files by giving a maximal page number which you think your most important documents have. The suggested number is 20.

```bash
Enter the maximal page number: 
```

2. `file_start` The default value is `1`.

   You could scrape pdf files in batches and later concate the output csv files from different batches together. To avoid having the same file number, please give an initial number for the file list. For example, if you scraped 10 pdf files last time and want to have new files scraped continuously, please type 11. 

```bash
Enter the start of the file number:
```

### 3.4. Output

The output is saved in `./data/output`. In this `output` directory, subdirectory `all_images`  contains all images, and those images with detected objects are saved in `all_images/detected`; subdirectory `lists` contains three CSV files, which list the PDF file information, the extracted image information and the skipped files (see 3.3.1.).



## 4. Other models

For uploading files larger than 100 Mb, please install [Git LFS](https://git-lfs.github.com/). See [more](https://stackoverflow.com/a/48734334/15390757).

For developing models for other insects, please contact the developer.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.