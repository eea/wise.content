<template>
  <div class="result-item" v-bind:class="typeClass">
      <div> {{ item.Type }}</div>
      <div style="font-weight: bold; margin: 2rem 0 2rem 1rem;">{{ item.Title }}</div>
      <button type="button" class="btn btn-primary details-button" @click="showModal = true">Details</button>
      <ModalDetails v-if="showModal" @close="showModal = false" :item="item">
      </ModalDetails>
  </div>
</template>

<script>
import ModalDetails from './ModalDetails.vue';
import typeClass from './ModalDetails.vue';
export default {
  components: { ModalDetails },
  props: [ 'item' ],
  data() {
    return {
      showModal: false
    }
  },
  computed: {
    typeClass() {
      return this.item.Type.toLowerCase().split(' ').join('-');
    }
  }
}
</script>

<style>
  .area {
    background-color: #fa6800;
  }

  .region {
    background-color: #dc4fad;
  }

  .competent-authority {
    background-color: #00aba9;
  }
  
  .marine-reporting-unit {
    background-color: #CE352C;
  }

  .result-item {
    float:left;
    color:white;
    margin: 5rem;
    padding:1rem; 
    width: 27rem;
    height: 17rem;
    font-size: 1.5rem;
    position:relative;
    border:0.1rem solid gray;
  }
  
  .result-item:hover {
    background-color: #60a917;
  }

  h5.result-item {
    font-weight: bold;
    margin: 2rem 0rem;
  }
  .details-button {
    font-size: 1.5rem;
    position: absolute;
    right: 0.5rem;
    bottom: 0.25rem;
    margin-right: 1rem; 
    margin-bottom: 1rem;
  }
  .details-button:hover {
    font-size: 1.55rem;
  }

  .result-table {
    font-size: 2rem;
  }
  .result-table > tr > td.key {
    font-weight: bold;
  }
  
  @media screen and (max-width: 1024px){
    .items-per-page {
      margin-left: 4.3rem;
      object-fit: cover;
    }
    .result-item {
      margin-left: 1.5rem;
    }
  }
</style>