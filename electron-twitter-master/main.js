// Loads Electron specific app that is not commonly available for node or io.js
var { app, ipcMain, BrowserWindow, crashReporter } = require("electron");

// Read our happy tweets
var Twitter = require("twitter");

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the javascript object is GCed.
var mainWindow = null;

process.env.TWITTER_CONSUMER_KEY = "20vKQdKcxCwEDySN5CKrAg1vs"
process.env.TWITTER_CONSUMER_SECRET = "rrVsGMOOH0SS2LLWWejHQj2G6QTVWCJk61PYt49m9LX0Nugi1p"
process.env.TWITTER_TOKEN_KEY = "1461876012-JOpd4PBU95wF2WGuy7LJKBlBZvtbHI4TxpgYget"
process.env.TWITTER_TOKEN_SECRET = "jpiJLj8JStwCT4UppWpKGUMwWCZiOKN0YSmICEWoB8Ock"
process.env.TWITTER_USER = "hrukalive"

// Quit when all windows are closed.
app.on("window-all-closed", function() {
    if (process.platform != "darwin") {
        app.quit();
    }
});

// This method will be called when Electron has done everything
// initialization and ready for creating browser windows.
app.on("ready", function() {
    crashReporter.start({
        productName: 'YourName',
        companyName: 'YourCompany',
        submitURL: 'https://your-domain.com/url-to-submit',
        uploadToServer: false
      });

    var client = new Twitter({
        consumer_key: process.env.TWITTER_CONSUMER_KEY,
        consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
        access_token_key: process.env.TWITTER_TOKEN_KEY,
        access_token_secret: process.env.TWITTER_TOKEN_SECRET
    });
    
    var params = {
        screen_name: process.env.TWITTER_USER || "hrukalive"
    };
    
    ipcMain.on('readTwitter', (event) => {
        // Query twitter for feed information
        client.get("statuses/user_timeline", params, function(error, tweets, response) {
            if (error) {
                console.log(error);
                return;
            }

            var textContentOfTweets = tweets.map(function(t) { return { text: t.text, user: t.user.screen_name }; });
            console.log(textContentOfTweets);
            event.sender.send("tweets", textContentOfTweets);
        });
    });

    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600
    });

    // and load the index.html of the app.
    mainWindow.loadURL("file://" + __dirname + "/index.html");
    // Emitted when the window is closed.
    mainWindow.on("closed", function() {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null;
    });

    // readTwitter.read(mainWindow);
});
