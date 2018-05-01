// Loads Electron specific app that is not commonly available for node or io.js
var { app, ipcMain, BrowserWindow, crashReporter } = require("electron");

// Read our happy tweets
var Twitter = require("twitter");

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the javascript object is GCed.
var mainWindow = null;

process.env.TWITTER_CONSUMER_KEY = "RATlQLeHrNY17mTuEL3eMEM3c"
process.env.TWITTER_CONSUMER_SECRET = "JWR6DEWyjOmvAFOIeglcHDEWv4olCzauMH59pBFWDa2bkZkSdg"
process.env.TWITTER_TOKEN_KEY = "988901359511580673-6HVb7DimhqR1VXSpI6VEB5D37ULw3HJ"
process.env.TWITTER_TOKEN_SECRET = "ZYrglSdFN9HE1sSb3BU0UUt5fHtGeRDsamRnehxQy58dO"
process.env.TWITTER_USER = "TestNormalizer"

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

    let client = new Twitter({
        consumer_key: process.env.TWITTER_CONSUMER_KEY,
        consumer_secret: process.env.TWITTER_CONSUMER_SECRET,
        access_token_key: process.env.TWITTER_TOKEN_KEY,
        access_token_secret: process.env.TWITTER_TOKEN_SECRET
    });
    
    let params = {
        with: 'followings',
        include_rts: 'false',
        extended_tweet: true
    };

    client.stream('user', params, (stream) => {
        console.log(stream)
        stream.on('data', (tweet) => {
            console.log(tweet)
        })
    });
    
    ipcMain.on('readTwitter', (event) => {
        // Query twitter for feed information
        client.get("statuses/filter.json", params, function(error, tweets, response) {
            if (error) {
                console.log(error);
                return;
            }
            var textContentOfTweets = tweets.map(t => { return { text: t.text, user: t.user.screen_name } });
            console.log(textContentOfTweets);
            event.sender.send("tweets", textContentOfTweets);
        });
    });

    mainWindow = new BrowserWindow({
        width: 800,
        height: 600
    });

    mainWindow.loadURL("file://" + __dirname + "/index.html");
    mainWindow.on("closed", function() {
        mainWindow = null;
    });
});
