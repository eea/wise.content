<template>
  <div class="vue_app">
    <country-data></country-data>
  </div>
</template>

<script>
  import axios from 'axios';
  import CountryData from './components/CountryData.vue';

export default {
  name: "CountriesSearch",
  components: {CountryData},
  mounted() {
    axios.get(window.ajax_target)
      .then(
        (response) => this.$emit('data-download', response.data)
        //CountryData.getUrl();
      );
  },
}
</script>

<style>
  .vue_app {
    margin: 0.5rem -2.5rem -2.5rem 0.5rem;
    font-family: 'Open Sans',Verdana,Helvetica,Arial,sans-serif;
  }
  #countries-list, #type-list {
    margin-top: 0.3125rem;
    padding-left: 0.5em;
  }
  .country-filter {
    width:60%;
  }
  .type-filter {
    width: 20%;
  }
  .country-filter, .type-filter {
    float:left;
    height: 16rem;
    margin-left: 2.2rem;
  }

  @media screen and (min-width: 1024px){        
    #countries-list {
      columns:3;
    }
    #type-list {
      margin-top: 2.9em;
      columns: 1;
    }
  }
  @media screen and (max-width: 1024px){
    li.country-item, li.type-item,
    #content li.country-item,
    #content li.type-item {
      font-size: 0.625rem;
    }
    #countries-list {
      columns:2;
    }
    #type-list {
      margin-top: 1rem;
      columns: 1;
    }
    .country-filter {
      width:90%;
      margin-right: 25rem;
      height: 220px;
    }
    .type-filter {
      width:90%;
      height: 85px;
     }
  }

  .facet-title-text {
    align-self: center;
    margin: 0 1.5em 1em 1.5em;
    display: block;
    color: #FFF;
    font-weight: bold;
  }

  .facet-title {
    width: 14.6rem;
    margin-right: 1.5rem;
    height:100%;
    float:left;
    background-color: #0071b3;
    -webkit-flex: 0.5;
    -moz-flex: 0.5;
    -ms-flex: 0.5;
    flex: 0.5;
    display: -webkit-flex;
    display: -moz-flex;
    display: -ms-flex;
    display: flex;
    position: relative;
    min-width: 2.1875rem;
    smargin-right: 1.25rem;
  }

  .facet-title:after {
    top: 42%;
    left: 100%;
    content: " ";
    height: 0;
    width: 0;
    position: absolute;
    pointer-events: none;
    border: 0.8125rem solid transparent;
    border-left-color: #0071b3;
  }

li.country-item, 
li.type-item,
#content li.country-item,
#content li.type-item {
  width:12rem;
  font-size:1.1rem;
  overflow:hidden;
  line-height:1.3em;
  margin-bottom:0.2em;
}
li.type-item,
#content li.type-item {
  width: 13rem;
}
input.country-checkbox, 
input.type-checkbox,
#content input.country-checkbox, 
#content input.type-checkbox{
  margin: 0.16rem 0 0;
  float:left;
}
.country-name, .type-name {
  float:left;
  margin-left: 0.25rem;
}
.country-count, .type-count {
  float:right; color:gray
}

.filter-wrapper {
  width: 100%
}

.items-per-page {
  margin-left: 1.5rem;
  width: 95%;
}

</style>
