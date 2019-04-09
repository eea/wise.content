<template>
    <div class="result-item">
        <table class="result-table">
            <tr v-for="field in result.fields" v-if="fields_whitelist.includes(field.key)">
                <td class="key">{{ field.name }}</td>
                <td class="value">{{ field.value }}</td>
            </tr>
        </table>
        <button class="details-button" @click="showModal = true">Details</button>
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
            fields_whitelist:['C_CD', 'MSCACode', 'CompetentAuthorityName', 'City'],
            showModal: false
        }
    }
}

</script>
<style>
    .result-item{border:1px solid gray;width:240px; float:left; height:300px; margin:3px; padding:3px; position:relative;}
    .details-button{position: absolute;right: 0;bottom: 0; margin-right:3px; margin-bottom:3px}
    .result-table {}
    .result-table > tr > td.key {font-weight: bold;}
</style>
