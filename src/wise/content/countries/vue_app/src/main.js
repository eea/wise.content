import Vue from 'vue'
import VueRouter from 'vue-router'
import CountriesSearch from './CountriesSearch'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    { path: '', component: CountriesSearch }
  ]
})

new Vue({
    router,
    el: '#countries-search',
    render: h => h(CountriesSearch)
})