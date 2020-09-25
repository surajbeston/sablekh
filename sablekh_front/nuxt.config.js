
export default {
  /*
  ** Nuxt rendering mode
  ** See https://nuxtjs.org/api/configuration-mode
  */
 server: {
  port: 8001, // default: 3000
  host: 'localhost' // default: localhost
},
  mode: 'universal',
  /*
  ** Nuxt target
  ** See https://nuxtjs.org/api/configuration-target
  */
  target: 'server',
  /*
  ** Headers of the page
  ** See https://nuxtjs.org/api/configuration-head
  */
  head: {
    title: 'Sablekh',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      // { name:"google-signin-client_id", content:"886662944835-islfqia69h4jtsqp060n533h8pkepu9u.apps.googleusercontent.com" }
      // { hid: 'description', name: 'description', content: "Sablekh is a platform to share small files easily in public." }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {href: "https://fonts.googleapis.com/css2?family=Comfortaa&family=Rajdhani&family=Staatliches&display=swap&family=Ubuntu:wght@300&display=swap" , rel: "stylesheet"},
      // { rel:"stylesheet", href:"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", integrity:"sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm", crossorigin:"anonymous" }
    ],
    script: [
      {src: 'https://apis.google.com/js/platform.js'}
    ]
  },
  /*
  ** Global CSS
  */
  css: [    // oh shit its here
  ],
  /*
  ** Plugins to load before mounting the App
  ** https://nuxtjs.org/guide/plugins
  */
  plugins: [{ src: '~plugins/ga.js', mode: 'client' }],
  /*
  ** Auto import components
  ** See https://nuxtjs.org/api/configuration-components
  */
  components: true,
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
  ],

  // auth: {
  //   strategies: {
  //       google: {
  //         client_id: '886662944835-islfqia69h4jtsqp060n533h8pkepu9u.apps.googleusercontent.com',
  //         redirect_uri: "http://localhost:8001/login",
  //       },
  //   }
  // },

  /*
  ** Build configuration
  ** See https://nuxtjs.org/api/configuration-build/
  */
  build: {
  },

}
