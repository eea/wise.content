<template>
  <div class="result-item" v-bind:class="typeClass()">
    <div> {{ item.Type }}</div>
    <div style="font-weight: bold; margin: 2rem 0 2rem 1rem;">{{ item.Title }}</div>
    <button type="button" class="btn btn-primary details-button" @click="showModal = true">Details</button>
    <ModalDetails v-if="showModal" @close="showModal = false" :item="item">
    </ModalDetails>
  </div>
</template>

<script>
import ModalDetails from './ModalDetails.vue';
export default {
  components: { ModalDetails },
  props: [ 'item' ],
  data() {
    return {      
      showModal: false
    }
  },
  methods: {
    typeClass() {
      return this.item.Type.toLowerCase().split(' ').join('-');
    }
  }
}

</script>
<style>
  .area {
    background-color: #ffdbe1a8;
  }
  .region {
    background-color: #a6d5ff54;
  }
  
  .competent-authority {
    background-color: #d6ffe13b;
  }
  
  .marine-reporting-unit {
    background-color: #fcffd47d;
  }
  
  .result-item {
    margin: 3.5rem;
    border:0.1rem solid gray;
    width: 27rem;
    float:left;
    height: 17rem;
    padding:1em; 
    position:relative;
    }
  
  h5.result-item {
    font-weight: bold;
     margin: 2rem 0rem 2rem 1rem;
  }
  
  .details-button {
    font-size: 1rem;
    position: absolute;
    max-height: 2.5rem;
    right: 0.5rem;
    bottom: 0.5rem;
    margin-right: 1rem; 
    margin-bottom: 1rem;
    }

  .result-table > tr > td.key {
    font-weight: bold;
    }
</style>