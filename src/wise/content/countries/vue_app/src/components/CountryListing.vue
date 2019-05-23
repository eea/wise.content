<template>
  <div class="results">
    <div style="clear:both"></div>
    <div style="margin-top: 1rem;margin-left: 2.2rem">
      <span style="margin-left: 3rem;">Results:</span> <span class="results-number">{{displayData.length}}</span>
    </div>
    <div style="margin-left: 3rem">
      <span style="margin-left: 2.2rem;"> Showing:</span>
      <span class="from-to">
        {{ page * batchSize}} -
        {{ Math.min(page * batchSize + batchSize, displayData.length)}}
      </span>
    </div>
    <div style="clear:both"></div>

    <div class="items-per-page">
      <pagination
        v-if="displayData.length > batchSize"
        :batch-size="batchSize"
        :page="page"
        :count="displayData.length"
        @onPageChanged="handlePageChanged">
      </pagination>

      <div style="clear:both"></div>
      <div v-for="item in pagedData">
        <item-tile :item='item'></item-tile>
      </div>
      <div style="clear:both"></div>
        <pagination
          v-if="displayData.length > batchSize"
          :batch-size="batchSize"
          :page="page"
          :count="displayData.length"
          @onPageChanged="handlePageChanged">
        </pagination>
    </div>
  </div>
</template>

<script>

import ItemTile from './ItemTile.vue'
import Pagination from './Pagination.vue';

export default {
  name: 'CountryListing',
  components: {
    ItemTile,
    Pagination
  },
  data () {
    return {
      'batchSize': 9,
      'page': 0,
    }
  },
  props: [
    'displayData',
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
