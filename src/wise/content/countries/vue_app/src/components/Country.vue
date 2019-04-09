<template>
    <li class="country-item">
        <input class="country-checkbox" type="checkbox" @change="updateValues" v-model="country.checked"></input>
        <div class="country-name"> {{country.name}} </div>
        <div class="country-count"> {{country.count}} </div>
    </li>
</template>

<script>

export default {
    props: ['country'],
    data() {
        return {}
    },
    methods: {
        updateValues() {
            this.$emit("countryChecked");
            debugger;
        }
    }
}

</script>

<style>

    li.country-item,
    #content li.country-item {
        width:150px;
        margin-bottom:0.2em;
        overflow:hidden;
        line-height:1.3em;
    }
    input.country-checkbox,
    #content input.country-checkbox {
        margin: 2px 0 0;
        float:left;
    }
    .country-name {
        float:left;
        padding-left:4px;
    }
    .country-count {float:right; color:gray}
</style>
