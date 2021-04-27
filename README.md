# Cornershop Backend Test
## Meals App

A simple but powerful django-app integrated with [Slack API](https://api.slack.com/), after installed you will able to:

- Create Meals
- Create a Menu with meals for an specific country
- Notify the Menu via Slack with a interactive message to receive preferences (Orders)
- Open or Close the menu or delete to create a new one

## Slack Pre-requisites 
1. A New SlackApp created in your Workspace
2. Add the next User Token scopes to your app.
```sh
    # User Token Scopes
        identify
        users:read
        users:read.email
```
3.  Add a interactive request url with https (you can use [ngrok](https://ngrok.com/)) to receive Slack Events
4.  Add this path to redirect_url /slack/login/ in order to complete the OAuth Flow

## Installation
Now you are ready to configure env vars and install the app
    
#### Step 1. Add ENV vars
Add the next Slack ENV Vars into docker-compose.yml with real values
```sh
       SLACK_CLIENT_ID
       SLACK_CLIENT_SECRET_ID
       SLACK_BOT_TOKEN 
       SLACK_OAUTH_REDIRECT_URI
```
#### Step 2. Run 
run commands in your terminal
```sh
      make up
      dev migrate
      dev up
```

## Usage

- Go to your web django app http://localhost:8000/ and interact with the UI

## Features
- A message interactive to Employees
![alt text](https://i.ibb.co/KWQGzQY/Sin-t-tulo.png)

## Libraries added

- [slack-sdk] - [Python Slack SDK](https://slack.dev/python-slack-sdk/)
- [model-bakery] - [Smart fixtures for better tests](https://github.com/model-bakers/model_bakery)
- [django-countries] -  Provides country choices for use with forms
- [Bootstrap] - [A more elegant presentation](https://github.com/SmileyChris/django-countries/)


## TODO:
-   Make the closing time of menus configurable by country
-   Reply to Employee after his preference action in the interactive message 
-   Add slash command to Bot Slack to receive a customization choose of User
-   Improve unitTesting 

## Developer
### Tomás Cornejo Corral