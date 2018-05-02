<template lang="html">
  <div id="sui-container" class="ui container">
    <sui-feed>
      <sui-feed-event v-for="(tweet, index) in tweets.slice().reverse()" :key="tweet.id">
        <sui-feed-label :image="tweet.user.profile_image_url" />
        <sui-feed-content>
          <sui-feed-summary>
            {{ tweet.user.name }} (@{{ tweet.user.screen_name }})
            <sui-feed-date>{{ dateFormat(tweet) }}</sui-feed-date>
          </sui-feed-summary>
          <sui-feed-extra text>
            {{ tweet.full_text }}
          </sui-feed-extra>
          <sui-feed-meta>
            <sui-feed-like>
              <sui-icon name="like" />
              {{ tweet.favorite_count }} Likes
            </sui-feed-like>
            <sui-feed-like>
              <sui-icon name="retweet" />
              {{ tweet.retweet_count }} Retweets
            </sui-feed-like>
            <sui-feed-like>
              <sui-icon name="reply" />
              {{ tweet.quote_count }} Quotes
            </sui-feed-like>
            <sui-button
              v-if="tweets[tweets.length - index - 1] && !tweets[tweets.length - index - 1].normalized"
              class="mini"
              :class="{ disabled: tweets[tweets.length - index - 1].triggered }"
              basic
              color="black"
              content="Normalize"
              @click="normalize(tweets.length - index - 1)"/>
            <sui-button
              v-if="tweets[tweets.length - index - 1] && tweets[tweets.length - index - 1].normalized"
              class="mini"
              basic
              color="teal"
              content="Revise"
              @click=""/>
          </sui-feed-meta>
        </sui-feed-content>
      </sui-feed-event>
    </sui-feed>
  </div>
</template>

<script>
const spawn = require('child_process').spawn
export default {
  name: 'test',
  data () {
    return {
      TWITTER_CONSUMER_KEY: "RATlQLeHrNY17mTuEL3eMEM3c",
      TWITTER_CONSUMER_SECRET: "JWR6DEWyjOmvAFOIeglcHDEWv4olCzauMH59pBFWDa2bkZkSdg",
      TWITTER_TOKEN_KEY: "988901359511580673-6HVb7DimhqR1VXSpI6VEB5D37ULw3HJ",
      TWITTER_TOKEN_SECRET: "ZYrglSdFN9HE1sSb3BU0UUt5fHtGeRDsamRnehxQy58dO",
      TWITTER_USER: "TestNormalizer",
      client: undefined,
      followers: [],
      tweets: [],
      text: ''
    }
  },
  methods: {
    normalize (idx) {
      this.tweets[idx].triggered = true
      const scriptExecution = spawn("python3", ["../normalize_tweets.py"])
      scriptExecution.stdout.on('data', (data) => {
        let tokens = String.fromCharCode.apply(null, data).split(/\r?\n/)
        this.tweets[idx].normalized = true
        this.tweets[idx].full_text = tokens.slice(Math.floor(tokens.length / 2), tokens.length - 1).join(' ')
        this.tweets[idx].input = tokens.slice(0, Math.floor(tokens.length / 2))
        this.tweets[idx].output = tokens.splice(Math.floor(tokens.length / 2), tokens.length - 1)
      });
      scriptExecution.stderr.on('data', (data) => {
        console.log(String.fromCharCode.apply(null, data))
      });

      scriptExecution.on('exit', (code) => {
        console.log("Process quit with code : " + code);
      });
      scriptExecution.stdin.write(this.tweets[idx].full_text);
      scriptExecution.stdin.end();
    },
    dateFormat (tweet) {
      let date = new Date(tweet.created_at)
      return date.getFullYear() + '-' + this.pad(date.getMonth() + 1) + '-' + this.pad(date.getDate())
        + ' ' + this.pad(date.getHours()) + ':' + this.pad(date.getMinutes()) + ':' + this.pad(date.getSeconds())
    },
    pad (n) {
      var s = n.toString()
      while (s.length < 2) {
        s = '0' + s
      }
      return s
    }
  },
  created () {
    var Twitter = require("twitter");
    this.client = new Twitter({
        consumer_key: this.TWITTER_CONSUMER_KEY,
        consumer_secret: this.TWITTER_CONSUMER_SECRET,
        access_token_key: this.TWITTER_TOKEN_KEY,
        access_token_secret: this.TWITTER_TOKEN_SECRET
    })
    this.client.get('friends/ids', { screen_name: this.TWITTER_USER }, (error, ids, response) => {
      if (!error) {
        this.client.get('statuses/home_timeline', {
          extended_tweet: 'full_text',
          tweet_mode: 'extended'
         }, (error, tweets, response) => {
          if (!error) {
            this.tweets = this.tweets.concat(tweets.map(t => {
              t.triggered = false
              t.normalized = false
              return t
            }).slice().reverse())
          }
        })
        this.client.stream('statuses/filter', {
          track: 'javascript',
          language: 'en'
        }, (stream) => {
          stream.on('data', (event) => {
            this.client.get('statuses/show/' + event.id_str, { id: event.id_str, tweet_mode: 'extended' }, (error, tweet, response) => {
              tweet.triggered = false
              tweet.normalized = false
              this.tweets.push(tweet)
            })
          })
          stream.on('error', (error) => {
            throw error
          })
        })
      }
    })
  },
  beforeDestory () {
    this.client.close()
  }
}
</script>
