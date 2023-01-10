# SETUP
<img alt="logo" height="150" src="static/image/mavefund.png" width="150"/>

#### the project and the database to run it locally, debug and fix errors


### note: 
#### if you have any of the components installed, its not mandatory to install them again

## Steps:
### **1. Docker**
* click this link to [download](https://www.docker.com/products/docker-desktop/)
docker ![[docker download]](/tmp/docker_download.png)
* after it is installed just open it and run it

### **2. Python 3.10**
* click this link to [download](https://www.python.org/downloads/release/python-3109/)
Python 3.10. scroll down a little and click the highlighted link: 
![[python download]](/tmp/python_download.png)
* > **make sure to TICK the box where it says to add python to the PATH environmental variables**

### **3. install Git and GitHub desktop**
* click this link to [download](https://git-scm.com/downloads) git. 
* click this link to [download](https://desktop.github.com) GitHub desktop. 
* after they are installed, sign in with your account

### **4. Clone this repository**
* using your favorite IDE, clone this repository somewhere nice and safe.
  * for **Jetbrains IDEs** use the new project button: ![jb ide get from vcs](/tmp/jbide_get_from_vcs.png)
  * for **VsCode** use the `clone_repository` button 
  ![vsc clone repo](/tmp/vsc_clone_repo.png)
    * in the tab put in this url: `https://github.com/ddjerqq/mavefund_api.git`. 
    * (note: give it some time to download for the first time)
    * after this you should have the project downloaded and open

### **5. Install requirements-setup.txt**
* run this in your terminal
    ```bash
    py -3.10 -m pip install -r requirements-setup.txt
    ```

### **6. Run setup.py**
* run this is your terminal again
    ```bash
    py -3.10 setup.py
    ```
* if the script is successful ✨**congratulations**✨ you are ready to move to the next step.
* if there are any errors, or exceptions raised let me know [@ddjerqq](https://github.com/ddjerqq) 
  on git or on discord [psyche#4876](https://discord.com)

### **6. Run the app**
* run this in your terminal to start postgres and the fastapi web app together.
    ```bash
    docker-compose up
    ```
