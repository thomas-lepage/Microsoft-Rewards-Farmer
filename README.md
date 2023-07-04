<p align="center">
  <img src="https://forthebadge.com/images/badges/made-with-python.svg"/>
  <img src="http://ForTheBadge.com/images/badges/built-by-developers.svg"/>
  <img src="http://ForTheBadge.com/images/badges/uses-git.svg"/>
  <img src="http://ForTheBadge.com/images/badges/built-with-love.svg"/>
</p>

<pre align="center">
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
       by Thomas Lepage (@charlesbel)          version 3.1.0
</pre>

<p align="center">
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge"/>
</p>

<h2 align="center">👋 Welcome to the future of automation</h2>
<h3 align="center">A simple bot that uses selenium to farm Microsoft Rewards written in Python.</h3>

<h2 align="center">Installation</h2>
<p align="center">
  <ul>
    <li>Install requirements with the following command : <pre>pip install -r requirements.txt</pre></li>
    <li>Make sure you have Chrome installed</li>
    <li>Install ChromeDriver :<ul>
      <li>Windows :<ul>
        <li>Download Chrome WebDriver : https://chromedriver.chromium.org/downloads</li>
        <li>Place the file in X:\Windows (X as your Windows disk letter)</li>
      </ul>
      <li>MacOS or Linux :<ul>
        <li><pre>apt install chromium-chromedriver</pre></li>
        <li>or if you have brew : <pre>brew cask install chromedriver</pre></li>
      </ul>
    </ul></li>
    <li>Edit the accounts.json.sample with your accounts credentials and rename it by removing .sample at the end<br/>
    If you want to add more than one account, the syntax is the following : <pre>[{
        "username": "Your Email",
        "password": "Your Password"
    },
    {
        "username": "Your Email 2",
        "password": "Your Password 2"
}]</pre></li>
    <li>Run the script</li>
   </ul>
</p>

<h2 align="center">Features</h2>
<p align="center">
<ul>
  <li>Bing searches (Desktop, Mobile and Edge) with User-Agents</li>
  <li>Complete automatically the daily set</li>
  <li>Complete automatically punch cards</li>
  <li>Complete automatically the others promotions</li>
  <li>Headless Mode</li>
  <li>Multi-Account Management</li>
</ul>
</p>

<h2 align="center">Hooks</h2>
<p align="center">
You can add hooks to do certain action when an account is completed with successor there is an error with an account. More hooks will come!
An example is set in the file hooks/hook.py. You can add as much files as you want in this folder to add all the function you want.
The example send an IFTTT notification.
</p>
<p align="center">
If you want to add your custom function on a hook, simply edit the hooks/hook.py file (but maybe overwritten when pulling updates), add a new file with your custom code. If you are using the docker-compose, the folder hooks is mounted as a volume so just put your files in the volume and they will be loaded.
</p>
<p align="center">
Available hooks
<ul>
  <li>account_completed</li>
  <li>account_error</li>
</ul>
</p>
