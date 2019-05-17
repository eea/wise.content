<template>
  <div>
    <div class="filter-wrapper">
      <country-filter
        :available-countries="countries"
        :preselected-countries="preselectedCountries"
        @selectionChange="updateCountryFilter">
      </country-filter>

      <type-filter
        :available-types="dataTypes"
        :preselected-types="preselectedTypes"
        @selectionChange="updateTypesFilter">
      </type-filter>
    </div>

    <country-listing
      :display-data="displayData"
      :preselected-countries="preselectedCountries"
      :preselected-types="preselectedTypes">
    </country-listing>
  </div>
</template>
<script>
import CountryFilter from './CountryFilter.vue';
import TypeFilter from './TypeFilter.vue';
import CountryListing from './CountryListing.vue';

export default {
  components: {
    CountryFilter,
    CountryListing,
    TypeFilter,
  },

  methods: {
    updateUrl(){
      this.$router.replace({
        path:	 "", 
        query: {
          c:this.countryFilter, 
          t:this.typesFilter
        }})
    },

    updateCountryFilter (codes) {
      // dirty trick, should refactor
      this.countryFilter = codes
      this.$children.forEach(c => {
        if (c.$options._componentTag == 'country-listing') {
          c.resetPage()
        }
      })
      this.updateUrl();
    },

    updateTypesFilter (types) {
      // dirty trick, should refactor
      this.typesFilter = types
      this.$children.forEach(c => {
        if (c.$options._componentTag == 'country-listing') {          
          c.resetPage()
        }
      })
      this.updateUrl();
    }
  },

  data () {
    return {
      'allData': [],
      'countryFilter': [],
      'typesFilter': [],
      'startPage': 0,
    }
  },

  mounted() {
    this.$parent.$on('data-download', (data) => {
      this.allData = data.results
    })
  },

  computed: {
    dataTypes () {
      let types = [];
      this.allData.forEach((r) => {
        if (types.indexOf(r.Type) == -1)
          types.push(r.Type)
      
      })
      return types;
    },
    displayData () {
      let data = this.allData
      let countries = this.countryFilter
      let types = this.typesFilter

      if (countries.length) {
        data = data.filter(r => countries.indexOf(r.CountryCode) > -1)
      }
      if (types.length) {
        data = data.filter(r => types.indexOf(r.Type) > -1)
      }
      return data
    },
    
    preselectedCountries() {
      let preCs = [];
      let countriesFromUrl = this.$route.query.c;
      if (typeof countriesFromUrl === 'undefined') {
        countriesFromUrl = [];
      } 
      else if (Array.isArray(countriesFromUrl)){
        countriesFromUrl.forEach(function(preC){
          preCs.push(preC);
        })
      }
      else {
        preCs.push(countriesFromUrl);
      }
      return preCs;
    },

    preselectedTypes() {
      let preTs = [];
      let typesFromUrl = this.$route.query.t;
      
      if (typeof typesFromUrl === 'undefined') {
        typesFromUrl = [];
      }
      else if (Array.isArray(typesFromUrl)){
        typesFromUrl.forEach(function(preT){
          preTs.push(preT);
        })
      }
      else {
        preTs.push(typesFromUrl);
      }
      return preTs;
    },

    countries () {
      let seen = {}
      let res = []

      for (let rec of this.allData) {
        if (!(rec.CountryCode in seen)) {
          let c = {
            name: rec.Country,
            code: rec.CountryCode,
            count: 1,
          }
          res.push(c)
          seen[rec.CountryCode] = c
        } else {
          seen[rec.CountryCode].count += 1
          // TODO: get count from displayData
        }
      }

      return res
    }
  }
}
</script>
