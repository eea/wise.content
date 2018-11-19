<template>
    <div class="results">

        <div><span> Results:</span> <span class="results-number">{{filtered_results.length}}</span> </div>
        <div><span> Showing:</span> <span class="from-to">{{ pos + 1}} - {{ Math.min(pos + batch_size, filtered_results.length)}}</span></div>
        <paginator v-if="filtered_results.length > batch_size" :batch_size="batch_size" :pos="pos" :count="filtered_results.length" @pageChanged="pageChanged"></paginator>
        <div style="clear:both"></div>
        <ItemList v-for="result in filtered_results.slice(pos, pos + batch_size)" :result="result" :key="result.MSCACode"></ItemList>
        <div style="clear:both"></div>
        <paginator v-if="filtered_results.length > batch_size" :batch_size="batch_size" :pos="pos" :count="filtered_results.length" @pageChanged="pageChanged"></paginator>

    </div>
</template>
<script>

import ItemList from './ItemList.vue';
import Paginator from './Paginator.vue';

export default {

    components: { ItemList, Paginator },

    props: [ 'countries', 'results', 'batch_size', 'pos' ],
    data() {
        return {}
    },
    computed: {
        selected_countries(){
            var tmp_countries = [];
            var all_countries = [];
            this.countries.forEach(function(country){
                if (country.checked){
                    tmp_countries.push(country.name);
                }
                all_countries.push(country.name);
            });
            if (tmp_countries.length == 0){
                tmp_countries = all_countries;
            }
            return tmp_countries;
        },
        filtered_results(){
            var tmp_results = [];
            var tmp_countries = this.selected_countries;
            this.results.forEach(function(result){
                if (tmp_countries.includes(result.country)){
                    tmp_results.push(result);
                }
            });
            return tmp_results;
        }
    },
    methods: {
        pageChanged(page) {
            this.$emit("pageChanged", page);
        }
    }

}


</script>
<style>
    .results {
        /*width:800px*/
    }
    .results-number,
    .from-to {
        font-weight:bold;
    }
</style>
