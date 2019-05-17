<template>
  <div class="results">
    <div style="clear:both"></div>
    <div style="margin-top: 1rem;margin-left: 2.2rem">
      <span>Results:</span> <span class="results-number">{{displayData.length}}</span>
    </div>
    <div style="margin-left: 2.3rem">
      <span> Showing:</span>
      <span class="from-to">
        {{ page * batchSize}} -
        {{ Math.min(page * batchSize + batchSize, displayData.length)}}
      </span>
    </div>
    <div style="clear:both"></div>

    <div class="items-per-page">
      <paginator
        v-if="displayData.length > batchSize"
        :batch-size="batchSize"
        :page="page"
        :count="displayData.length"
        @onPageChanged="handlePageChanged">
      </paginator>

      <div style="clear:both"></div>
      <div v-for="item in pagedData">
        <item-tile :item='item'></item-tile>
      </div>
      <div style="clear:both"></div>
        <paginator
          v-if="displayData.length > batchSize"
          :batch-size="batchSize"
          :page="page"
          :count="displayData.length"
          @onPageChanged="handlePageChanged">
        </paginator>
    </div>
  </div>
</template>

<script>
import ItemTile from './ItemTile.vue'
import Paginator from './Paginator.vue';

export default {
  name: 'CountryListing',
  components: {
    ItemTile,
    Paginator
  },
  data () {
    return {
      'batchSize': 20,
      'page': 0,
    }
  },
  props: [
    'displayData',
    'preselectedCountries',
    'preselectedTypes'
  ],
  computed: {
    pagedData() {
      let b = this.batchSize
      let p = this.page
      return this.displayData.slice(b * p, b * p + b)
    }
  },
  methods: {
    handlePageChanged (page) {
      this.page = page
    },
    resetPage () {
      this.page = 0
    }
  }
}
</script>

<style>
</style>
