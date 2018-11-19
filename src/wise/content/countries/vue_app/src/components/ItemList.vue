<template>
    <div class="result-item">
        <div v-for="field in result.fields" v-if="fields_whitelist.includes(field.key)" :class="field.key">
            {{ field.value }}
        </div>
        <div style="clear:both"> </div>
        <div class="details-button" @click="showModal = true">Details</div>
        <ModalDetails v-if="showModal" @close="showModal = false" :result="result">
        </ModalDetails>
    </div>
</template>
<script>

import ModalDetails from './ModalDetails.vue';

export default {

    components: { ModalDetails },

    props: [ 'result' ],
    data() {
        return {
            fields_whitelist:['MSCACode', 'CompetentAuthorityName', 'Responsibilities'],
            showModal: false
        }
    }
}

</script>
<style>
    .result-item{
        width:100%;
        float:left;
        min-height:100px;
        margin:3px;
        padding:3px;
        position:relative;
        border-bottom: 1px dotted #cccccc;
        padding-top: 0.5em;
    }
    .details-button{
        cursor:pointer;
        font-size:12px;
        position:absolute;
        margin-left:20px;
        bottom:10px;
        left:0px;
    }
    .details-button:before{
        content: "\f138";
        font-family: FontAwesome;
        font-size: 16px;
        color: gray;
        position: absolute;
        margin-left: -18px;
        top: -3px;
    }
    .MSCACode {
        font-weight: bold;
        font-size:12px;
    }
    .CompetentAuthorityName {
        color:#346f83;
        font-size:18px;
        font-weight: bold;
        padding-bottom: 10px;
    }
    .Responsibilities {
        font-size: 1.4em;
        color: #666;
        display:block;
        overflow:hidden;
        margin-bottom:30px;
    }
</style>
