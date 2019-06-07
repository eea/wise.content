<template>
  <div>
    <div class="result-item">
      <div>
        <div class="item-title">
          {{item.Type}}: {{item.Title}}
        </div>
        <ModalDetails v-if="showModal" @close="showModal = false" :item="item"></ModalDetails>
        <button type="button" class="btn btn-primary details-button" @click="showModal = true">Details</button>
      </div>
      <div class="image"></div>
    </div>
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
}
</script>

<style>
  .result-item {
    float: left;
    color: white;
    width: 27rem;
    height: 20rem;
    display: block;
    font-size: 1.5rem;
    position: relative;
    border: 0.1rem solid gray;
}

  .image {
    margin-top:4rem;
    height: 80%;
    display: block;
    overflow: hidden;
    background-size: cover;
    background-position: center center;
    background-image: url("https://www.eea.europa.eu/portal_depiction/country-profile/image_preview");
  }

  .item-title {
    top: 0;
    left: 0;
    right: 0;
    width: 26.8rem;
    padding: 5px;
    text-align:center;
    position: absolute;
    display: inline-block;
    vertical-align: middle;
    background-color: #009590;
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
    .result-item {
      margin: 1rem;
    }
    .items-per-page {
      width: 100%;
      object-fit: cover;
      margin-left: 4.3rem;
    }
  }
  @media screen and (min-width: 1024px){
    .result-item {
      margin: 3rem;
    }
  }
</style>