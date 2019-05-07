<template>
    <div class="vue_app">
        <div class="facet_group">
            <div class="facet_title">
                <span class="facet_title-text">
                    Select country
                </span>
            </div>
            <ul id="countries-list">
                    <Country v-for="country in countries" :country="country" :key="country.name" @countryChecked="countryChecked">
                    </Country>
            </ul>            
            <ul id="MRU-data">
                <MRU v-for="MRU in MRUs" :MRU="MRU" :key="MRU.key" @MRUChecked="MRUChecked">
                </MRU>
            </ul>
        <div style="clear:both"></div>
        </div>
        <div style="clear:both"></div>
        <div id="search-results">
            <Results :countries="countries" :results="results" :batch_size="batch_size" :pos="pos" @pageChanged="pageChanged"></Results>
        </div>
    </div>
</template>

<script>

import Country from './components/Country.vue';
import Results from './components/Results.vue';
import MRU from './components/MRU.vue';
import axios from 'axios';

export default {
    name: "CountriesSearch",
    components: {Country, Results, MRU},
    data() {
        return {
            countries : [],
            MRUs: [], 
            batch_size: 10,
            pos: 0,
            results : []}
    },
    mounted() {
        axios.get('http://localhost:5080/Plone/marine/countries-search-countries-list')
        axios.get(window.ajax_target)
            .then(function(response) {
                console.log(response);
                this.countries = response.data.y2012.countries;
                this.results = response.data.y2012.competentauthorities;
                this.MRUs = response.data.y2018.MarineReportingUnits;
                this.getUrlQuery()
            }
            .bind(this)
        );
    },
    methods: {
        MRUChecked() {
            this.pos = 0;
            this.setUrlQuery();
        },
        countryChecked() {
            this.pos = 0;
            this.setUrlQuery();
        },
        pageChanged(page) {
            this.$emit("pageChanged", this.page);
            this.pos = (page - 1) * this.batch_size;
            this.setUrlQuery();
        },
        setUrlQuery(){
            var tmp_page = this.pos/this.batch_size + 1
            var tmp_selected_countries = []
            this.countries.forEach(function(country){
                if (country.checked){
                    tmp_selected_countries.push(country.code);
                }
            });
            var tmp_selected_MRUs = []
            this.MRUs.forEach(function(MRU){
                if (MRU.checked){
                    tmp_selected_MRUs.push(MRU.code);
                }
            });            
            var query = {};
            if (tmp_page > 1){
                query.page = tmp_page;
            }
            if (tmp_selected_countries.length < this.countries.length) {
                query.country = tmp_selected_countries;
            }
            if (tmp_selected_MRUs.length < this.MRUs.length) {
                query.MRU = tmp_selected_MRUs;
            }
            this.$router.replace({ path: '', query: query})
        },        
        getUrlQuery(){
            this.pos = ((this.$route.query.page || 1)- 1) * this.batch_size;
            var countries = this.$route.query.country;
            if (countries !== undefined){
                this.countries.forEach(function(country){
                    if (countries.includes(country.code)){
                        country.checked = true;
                    }
                    else {
                        country.checked = false;
                    }
                });
            }
            var MRUs = this.$route.query.MRU;
            if (MRUs !== undefined){
                this.MRUs.forEach(function(MRU){
                    if (MRUs.includes(MRU.code)){
                        MRU.checked = true;
                    }
                    else {
                        MRU.checked = false;
                    }
                });
            }
        }
    }
}

</script>


<style>

    #countries-list, #MRU-data {
        margin-top:5px;
    }
    .facet_group {
        width:100%;
        height: 370px !important;
        float:left; 
        background-color:#F6FAFD;
    }
@media screen and (min-width: 1024px){
    #countries-list, #MRU-data {
        columns:3;
    }
    .facet_group {
        height:165px;
    }
}
@media screen and (max-width: 1024px){
    #countries-list, #MRU-data {
        columns:2;
    }
    .facet_group {
        height:330px;
    }
}
    .countries-list-column {
        float:left;
        padding-left:30px;
    }


    .facet_title-text {
        align-self: center;
        margin-left: 2em;
        display: block;
        color: #FFF;
        font-weight: bold;
    }

    .facet_title {
        width:150px;
        height:100%;
        float:left;
        background-color: #009590;
        -webkit-flex: 0.5;
        -moz-flex: 0.5;
        -ms-flex: 0.5;
        flex: 0.5;
        display: -webkit-flex;
        display: -moz-flex;
        display: -ms-flex;
        display: flex;
        position: relative;
        min-width: 115px;
        margin-right: 20px
    }

    .facet_title:after {
        top: 45%;
        left: 100%;
        content: " ";
        height: 0;
        width: 0;
        position: absolute;
        pointer-events: none;
        border: 13px solid transparent;
        border-left-color: #009590;
    }

    .vue_app {
        font-family: 'Open Sans',Verdana,Helvetica,Arial,sans-serif;
    }

</style>
