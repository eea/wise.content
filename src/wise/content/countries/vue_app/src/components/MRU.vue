<template>
    <li class="MRU-item">
        <input class="MRU-checkbox" type="checkbox" @change="updateValues" v-model="MRU.checked"></input>
        <div class="MRU-name"> {{MRU.CountryCode}} </div>
    </li>
</template>

<script>

export default {
    props: ['MRU'],
    data() {
        return {}
    },
    methods: {
        updateValues() {
            this.$emit("MRUChecked");
        }
    }
}

</script>

<style>

    li.MRU-item,
    #content li.MRU-item {
        width:150px;
        margin-bottom:0.2em;
        overflow:hidden;
        line-height:1.3em;
    }
    input.MRU-checkbox,
    #content input.MRU-checkbox {
        margin: 2px 0 0;
        float:left;
    }
    .MRU-name {
        float:left;
        padding-left:4px;
    }
    .MRU-count {float:right; color:gray}
</style>
