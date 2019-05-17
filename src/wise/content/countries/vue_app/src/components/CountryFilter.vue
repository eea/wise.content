<template>
  <div class="country-filter">
    <div class="facet-title">
      <span class="facet-title-text">
        Select country
      </span>
    </div>
    <div>
      <ul id="countries-list">
        <li class="country-item" v-for="country in availableCountries">
          <input
            class="country-checkbox"
            type="checkbox"
            v-bind:checked="isChecked(country.code)"
            @change="updateSelection(country.code)"
            ></input>
          <div class="country-name"> {{country.name}} </div>
          <div class="country-count"> {{country.count}} </div>
        </li>
      </ul>
      <div>{{preselectedCountries}}</div>
    </div>
  </div>
</template>
<script>
  export default {
    props: [
      'availableCountries',
      'preselectedCountries'
    ],
    data () {
      return {
        'selectedCountries': this.preselectedCountries
      }
    },
    methods: {
      updateSelection(code) {
        let data = this.selectedCountries;
        let ix = data.indexOf(code)
        if (ix == -1) {          
          data.push(code)
        } 
        else {
          data = data.filter(c => c != code)
        }
        this.selectedCountries = data
        this.$emit("selectionChange", data)
      },
      isChecked(code) {
        return this.preselectedCountries.indexOf(code) > -1
      }
    }
  }
</script>
<style>
</style>
