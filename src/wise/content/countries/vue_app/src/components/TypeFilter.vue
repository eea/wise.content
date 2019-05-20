<template>
  <div class="type-filter">
    <div class="facet-title">
      <span class="facet-title-text">
        Select info type
      </span>
    </div>
    <div style="vertical-align: center">
      <ul id="type-list">
        <li class="type-item" v-for="section in availableTypes">
          <input
            class="type-checkbox"
            type="checkbox"
            v-bind:checked="isChecked(section)"
            @change="updateSelection(section)"
            ></input>
          <div class="type-name"> {{section}} </div>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
  export default {
    props: [
      'availableTypes',
      'preselectedTypes'
    ],
    data () {
      return {
        'selectedTypes': this.preselectedTypes
      }
    },
    methods: {
      updateSelection(code) {
        let data = this.selectedTypes;
        let ix = data.indexOf(code)
        if (ix == -1) {
          data.push(code)
        } else {
          data = data.filter(c => c != code)
        }
        this.selectedTypes = data
        this.$emit("selectionChange", data)
      },
      isChecked(t) {
          return this.preselectedTypes.indexOf(t) > -1
      }
    }
  }
</script>
<style>
#type_filter {
  height: inherit !important;
}
</style>
