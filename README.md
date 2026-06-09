# Firebase Setup Guide for DataSlate Preview

This guide explains how to connect the **DataSlate Preview** app to Firebase.

It is written for a person who has never used Firebase before. Follow the steps in order.

The screenshots used in this guide are available here:

[Firebase_Screens folder](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/01.jpg)

Important: this guide uses a very simple setup for a preview version. It is easy to follow, but it is not secure.

---

# Important warning about security

This guide uses simple Firebase Rules for a preview version.

These Rules are **not secure**.

They allow anyone who knows the Firebase project configuration to read and write data in the Firestore database.

Use this setup only for:

- a test Firebase account,
- a preview version,
- a project with no private data,
- a temporary demo.

Do **not** use these Rules for a real production app with private or user data.

---

# Part 1 — Create a Firebase project

## Step 1 — Open Firebase

Open Firebase in your browser.

You should see the Firebase welcome page.

Find the large card named:

**Get started by setting up a Firebase project**

Click that card.

Screenshot: [01.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/01.jpg)

---

## Step 2 — Enter the project name

A window named **Create a project** will appear.

Find the field named:

**Project name**

Click inside that field.

Type this project name:

    RPG-DataSlate-Relay

Under the project name, Firebase will also show the project ID.

It should look similar to this:

    rpg-dataslate-relay

Find the checkbox named:

**I accept the Firebase terms**

Make sure this checkbox is checked.

Find the switch named:

**Join the Google Developer Program**

Leave this switch turned off.

Click:

**Continue**

Screenshot: [02.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/02.jpg)

---

## Step 3 — Turn off Gemini in Firebase

You will see a screen named:

**AI assistance for your Firebase project**

Find the option named:

**Enable Gemini in Firebase**

Leave this switch turned off.

Click:

**Continue**

Screenshot: [03.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/03.jpg)

---

## Step 4 — Turn off Google Analytics

You will see a screen named:

**Google Analytics for your Firebase project**

Find the option named:

**Enable Google Analytics for this project**

Leave this switch turned off.

Click:

**Create project**

Screenshot: [04.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/04.jpg)

---

## Step 5 — Wait until the project is ready

Firebase will create the project.

Wait until you see this message:

**Your Firebase project is ready**

Click:

**Continue**

Screenshot: [05.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/05.jpg)

Firebase may show the same “project is ready” screen in a slightly different size. This is normal.

Screenshot: [06.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/06.jpg)

---

# Part 2 — Add a web app to the Firebase project

## Step 6 — Open the project page

After clicking **Continue**, you will enter the Firebase project page.

The project name should be visible near the top:

    RPG-DataSlate-Relay

Under the project name, find the button:

**+ Add app**

Click:

**+ Add app**

Screenshot: [07.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/07.jpg)

---

## Step 7 — Select the Web app

A row of platform icons will appear.

Find the icon with this symbol:

    </>

Click the `</>` icon.

This is the Web app option.

Screenshot: [08.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/08.jpg)

---

## Step 8 — Register the web app

A window named **Add Firebase to your web app** will appear.

Find the field named:

**App nickname**

Click inside that field.

Type:

    DataSlate_Preview

Find the checkbox named:

**Also set up Firebase Hosting for this app**

Leave this checkbox unchecked.

You do not need Firebase Hosting for this guide, because the app is already hosted on GitHub Pages.

Click:

**Register app**

Screenshot: [09.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/09.jpg)

---

## Step 9 — Show and copy the Firebase configuration

Firebase will show a section named:

**Add Firebase SDK**

Find the option:

**Use a `<script>` tag**

Click it.

You will see a code box with the Firebase configuration.

Inside that code box, you will see lines similar to these:

    const firebaseConfig = {
      apiKey: "...",
      authDomain: "...",
      projectId: "...",
      storageBucket: "...",
      messagingSenderId: "...",
      appId: "..."
    };

Click the copy icon in the lower-right corner of the code box.

This copies the Firebase configuration to your clipboard.

After copying the configuration, click:

**Continue to console**

Screenshot: [10.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/10.jpg)

---

## Step 10 — Find the web app again later

After returning to the project page, you should see a button named:

**1 app**

Click:

**1 app**

Screenshot: [11.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/11.jpg)

A small panel will open.

It will show your app:

**DataSlate_Preview**

On the right side of that app row, click the small gear icon.

Screenshot: [12.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/12.jpg)

You will see the app settings page.

Find the section named:

**SDK setup and configuration**

Select:

**Config**

This shows the Firebase configuration again.

Screenshot: [13.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/13.jpg)

---

# Part 3 — Add Firebase configuration to GitHub

## Step 11 — Open the configuration file in GitHub

Open your GitHub repository.

Go to this file:

    DataSlate/config/firebase-config.js

Before editing, the file contains placeholder values.

They look like this:

    window.firebaseConfig = {
      apiKey: "INSERT_YOUR_API_KEY",
      authDomain: "INSERT_YOUR_AUTH_DOMAIN",
      projectId: "INSERT_YOUR_PROJECT_ID",
      storageBucket: "INSERT_YOUR_STORAGE_BUCKET",
      messagingSenderId: "INSERT_YOUR_MESSAGING_SENDER_ID",
      appId: "INSERT_YOUR_APP_ID",
    };

Screenshot: [14.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/14.jpg)

---

## Step 12 — Replace the placeholder values

Edit the file:

    DataSlate/config/firebase-config.js

Replace the placeholder values with the values copied from Firebase.

Important: keep the beginning exactly like this:

    window.firebaseConfig = {

Do **not** change it to this:

    const firebaseConfig = {

The DataSlate app needs the configuration to be stored in:

    window.firebaseConfig

The final file should look similar to this:

    window.firebaseConfig = {
      apiKey: "YOUR_API_KEY",
      authDomain: "YOUR_AUTH_DOMAIN",
      projectId: "YOUR_PROJECT_ID",
      storageBucket: "YOUR_STORAGE_BUCKET",
      messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
      appId: "YOUR_APP_ID"
    };

Replace the `YOUR_...` values with the real values from Firebase.

Save the file.

Commit the change to GitHub.

When the file is updated correctly, it should show real Firebase values instead of `INSERT_YOUR_...`.

Screenshot: [15.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/15.jpg)

---

# Part 4 — Create the Firestore database

## Step 13 — Open Cloud Firestore

Go back to Firebase.

Look at the menu on the left side.

Find:

**Firestore**

Click:

**Firestore**

You should see the Cloud Firestore page.

Click:

**Create database**

Screenshot: [16.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/16.jpg)

---

## Step 14 — Select Standard edition

A window named **Create a database** will appear.

In step 1, named **Select edition**, choose:

**Standard edition**

Do not choose **Enterprise edition**.

Click:

**Next**

Screenshot: [17.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/17.jpg)

---

## Step 15 — Select the database location

In step 2, named **Database ID & location**, leave the database ID as:

    (default)

Find the field named:

**Location**

Choose:

    eur3 (Europe)

Firebase will show a warning that the location cannot be changed later. This is normal.

Click:

**Next**

Screenshot: [18.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/18.jpg)

---

## Step 16 — Start in production mode

In step 3, named **Configure**, select:

**Start in production mode**

Do not select **Start in test mode**.

Click:

**Create**

Screenshot: [19.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/19.jpg)

---

## Step 17 — Wait for the empty database

After the database is created, Firebase will open the **Data** tab.

At this point the database is empty.

This is normal.

Do not click **Start collection**.

The DataSlate app will create the needed data automatically when you send the first test message.

Screenshot: [20.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/20.jpg)

---

# Part 5 — Set simple preview Rules

## Step 18 — Open the Rules tab

At the top of the Firestore page, click:

**Rules**

Firebase will show the default Rules.

The default Rules block all reading and writing.

Screenshot: [21.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/21.jpg)

---

## Step 19 — Replace the default Rules

Click inside the Rules editor.

Delete everything in the editor.

Paste this:

    rules_version = '2';

    service cloud.firestore {
      match /databases/{database}/documents {
        match /{document=**} {
          allow read, write: if true;
        }
      }
    }

After pasting, Firebase will show:

**unpublished changes**

Click:

**Publish**

Screenshot: [22.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/22.jpg)

---

## Step 20 — Confirm the public Rules warning

Firebase will show a red warning.

The warning says that the Rules are public.

This is expected for this simple preview setup.

These Rules have no real protection.

Use them only for a test project with no private data.

Screenshot: [23.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/23.jpg)

---

# Part 6 — Test the DataSlate app

## Step 21 — Open the DataSlate launcher

Open the DataSlate launcher in your browser.

Use this address:

    https://cutelittlegoat.github.io/rpg-dataslate-relay/DataSlate/index.html

You should see the page named:

**DATASLATE LAUNCHER**

Screenshot: [24.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/24.jpg)

---

## Step 22 — Open the GM panel

On the launcher page, find the section named:

**Production versions**

Click:

**Open GM**

The GM panel will open.

This is the screen used by the game master to send a message to the players.

Find the field named:

**Message content**

Click inside that field.

Type a test message, for example:

    Test message

Click:

**Send**

At the bottom-left, the status should change to:

    sent

Screenshot: [25.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/25.jpg)

---

## Step 23 — Open the DataSlate player view

Go back to the launcher page.

Find the section named:

**Production versions**

Click:

**Open DataSlate**

The DataSlate screen will open.

You should see the test message on the DataSlate screen.

Example message:

    Test message

Screenshot: [26.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/26.jpg)

---

## Step 24 — Check that Firebase received the message

Go back to Firebase.

Open:

**Cloud Firestore**

Click the tab:

**Data**

You should now see a collection named:

    dataslate

Click:

**dataslate**

Inside it, you should see a document named:

    current

Click:

**current**

On the right side, Firebase will show the fields created by the GM panel.

This confirms that the connection works.

Screenshot: [27.jpg](https://cutelittlegoat.github.io/rpg-dataslate-relay/Firebase_Screens/27.jpg)

---

# Final result

The setup is complete when all of these are true:

- the Firebase project exists,
- the web app `DataSlate_Preview` exists,
- the file `DataSlate/config/firebase-config.js` contains real Firebase values,
- Cloud Firestore exists,
- the Rules were published,
- the launcher opens from GitHub Pages,
- the GM panel can send a message,
- the DataSlate screen displays the message,
- Firestore shows `dataslate/current`.

---

# Troubleshooting

## The GM panel shows an error

Check this file:

    DataSlate/config/firebase-config.js

Make sure it contains real Firebase values.

Make sure it starts with:

    window.firebaseConfig = {

It should not start with:

    const firebaseConfig = {

---

## The message does not appear on the DataSlate screen

Check these things:

1. Make sure Firestore Rules were published.
2. Make sure the Rules contain this line:

       allow read, write: if true;

3. Make sure you clicked **Send** in the GM panel.
4. Refresh both browser tabs.
5. Wait one minute and refresh GitHub Pages again.

---

## The Firestore database is empty

This is normal before the first message is sent.

Open the GM panel.

Type a message.

Click:

**Send**

After that, Firestore should create:

    dataslate/current

---

## The browser still shows the old version

GitHub Pages may need a short moment to update.

Wait one minute.

Then refresh the page.

On Windows, press:

    Ctrl + F5

This forces the browser to reload the page.
