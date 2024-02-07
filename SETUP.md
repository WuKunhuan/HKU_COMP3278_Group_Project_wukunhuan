
# COMP3278 Facial Login Component · Setup Guideline

## 1. Setup Gitlab and Download the Package (in VSCode)

One recommended way to setup Gitlab in VSCode is as follows: 

- On Gitlab, click the avatar on the top right corner, then click <ins>Edit Profile -> Access Tokens -> add a token in Token Name field, click all Select scopes, and Create personal access token</ins>

- On top of VSCode, click <ins>View -> Command Palette -> Gitlab: Add Account to VSCode</ins>. When VSCode require the access token, paste the token generated in the above step. 

- In VSCode Extensions, search <ins>GitLab Workflow</ins> and download the extension. 

- In VSCode, <ins>View -> Command Palette -> Git: Clone</ins>. Enter the following link: https://gitlab.com/comp3278-1a-group2/comp3278-facial-login-component/-/blob/WuKunhuan_branch4. 

- In VSCode, select the destination of the cloned folder. Wait for the cloning to be finished, and then select open the folder. 

## 2. Get Facial Login Data

If you use VSCode to download the project, <ins>open an integrated terminal on top of the "codes/facial_login_data"</ins> folder. 

If you directly downloaded the project, <ins>open a terminal/command prompt on top of the "codes/facial_login_data"</ins> folder. 

Enter the following command in the terminal: 

```python face_capture.py```

It will let you to enter a username, and number of images to capture (Recommended 400). 

After the capturing, enter the following command in the terminal to train the recognizer: 

```python train.py```

## 3. Start the Program. 

Close the previous terminal and open a new terminal on top of the "codes"</ins> folder. 

Enter the following command to start the program: 

```python main.py```

Recognized user will be available to login. 

