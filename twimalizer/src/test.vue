<template>
  <sui-feed>
    <sui-feed-event v-for="tweet in tweets" :key="tweet.id">
      <sui-feed-label :image="tweet.user.profile_image_url" />
      <sui-feed-content>
        <sui-feed-summary>
          {{ tweet.user.name }} (@{{ tweet.user.screen_name }})
          <sui-feed-date>{{ dateFormat(tweet) }}</sui-feed-date>
        </sui-feed-summary>
        <sui-feed-extra text>
          {{ tweet.text || tweet.full_text }}
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
        </sui-feed-meta>
      </sui-feed-content>
    </sui-feed-event>
  </sui-feed>
</template>

<script>
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
    dateFormat (tweet) {
      let date = new Date(parseInt(tweet.timestamp_ms))
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
            this.tweets = this.tweets.map((tweet) => {
              tweet.text = tweet.full_text
              return tweet
            })
            this.tweets = this.tweets.concat(tweets)
            console.log(tweets)
            this.client.get('statuses/show', { id: tweets[0].id }, (error, tmp, response) => {
              console.log(tmp)
            })
          }
        })
        this.client.stream('statuses/filter', {
          track: 'javascript',
          language: 'en',
          extended_tweet: 'full_text',
          tweet_mode: 'extended'
          // follow: ids.ids.join(',')
        }, (stream) => {
          stream.on('data', (event) => {
            console.log(event)
            this.tweets.unshift(event)
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
