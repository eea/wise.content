<template>
  <div>
    <div class="result-item">
      <div>
        <div class="item-title">
          <div>{{item.Type}}: {{item.Title}}</div>
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
  .result-item{
    float:left;
    color:white;
    margin: 1rem;
    width: 27rem;
    padding: 2rem;
    height: 17rem;
    display: block;
    font-size: 1.5rem;
    position:relative;
    border:0.1rem solid gray;
  }

  .image {
    height: 90%;
    display: block;
    overflow: hidden;
    background-size: cover;
    background-image: url("https://www.eea.europa.eu/portal_depiction/country-profile/image_preview");
  }

  .item-title {
    text-align:center;
    height: 4.5rem;
    // line-height: 4.5rem;
    width: 26.8rem;
    margin: -2rem 0 0rem -2rem;
    background-color: #009590;
  }
  .item-title p {
    display: inline-block;
    vertical-align: middle;
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