<template>
  <div class="pagination-container">
    <div class="pagination">
      <div style="clear:both"></div>
      <div v-if="page > 0"
        class="prev-page-link"
        @click="goToPrevPage">Previous</div>

      <template v-for='index in pageNumbers'>
        <div
          v-if="index != -1"
          @click="changePage(index)"
          v-bind:class="{lastpage : index == pages - 1}"
          class="page-link">
          <span v-bind:class="{active : index == page} ">{{ index }}</span>
        </div>
        <div v-if="index == -1" class="page-link">
          <span>...</span>
        </div>
      </template>

      <div
        v-if="page < (pages - 1)"
        class="next-page-link"
        @click="goToNextPage">Next</div>

      <div style="clear:both"></div>
    </div>
  </div>
</template>

<script>
  export default {

    components: {},

    props: [ 'count', 'page', 'batchSize' ],
    computed: {
      pages(){
        return Math.ceil(this.count / this.batchSize);
      },
      pageNumbers () {
        let res = []

        for (var x = 0; x < this.pages; x++ ) {
          if (x < 3) {
            res.push(x)
            continue
          }
          if (x > this.pages - 3) {
            res.push(x)
            continue
          }
          if (x > this.page - 2 && x < this.page + 2) {
            res.push(x)
            continue
          }

          res.push(-1)
        }
        res = res.filter((el, i) => el !== res[i - 1])
        return res
      }
    },
    methods: {
      goToPrevPage(){
        this.$emit("onPageChanged", this.page - 1)
      },
      goToNextPage(){
        this.$emit("onPageChanged", this.page + 1)
      },
      changePage(page) {
        this.$emit("onPageChanged", page);
      }
    }
  }

</script>

<style>
.pagination-container {
  width:100%;
  text-align:center;
}
.pagination {
  display:inline-block;
}
.prev-page-link,
.next-page-link {
  display:block;
  float:left;
  cursor:pointer;
  font-size:4re,;
  border:0.1rem solid gray;
  padding:0.3rem;
  text-align:center;
  margin:0;
  color:gray;
  padding-left:2rem;
  padding-right:2rem;
  user-select: none;
}
.prev-page-link:hover,
.next-page-link:hover {
  background-color:#eee;
}

.page-link {
  display:block;
  float:left;
  cursor:pointer;
  font-size: 1.4rem;
  padding: 0.3rem;
  border: 0.1rem solid gray;
  text-align:center;
  width: 5.5rem;
  margin:0;
  color:gray;
  user-select: none;
}
.page-link:hover {
  background-color:#eee;
}
.page-link:has(.active) {
  background-color: pink;
}
.lastpage {
  border-right: 0.1rem solid gray;
}
span.active {
  color:#346f83;
  font-weight:bold;
}
</style>
