<template>
    <div class="page-link" @click="changePage" v-bind:class="{lastpage : isLast}">
        <span v-bind:class="{active : isActive}">{{ page }}</span>
    </div>
</template>

<script>

export default {

    props: [ 'page', 'current_page', 'count' ],
    data() {
        return {}
    },
    methods: {
        changePage() {
            this.$emit("pageChanged", this.page);
       }
    },
    computed: {
        isLast() {
            return this.current_page == this.count;
        },
        isActive(){
            return this.page==this.current_page;
        }
    }
}

</script>

<style>
    .page-link {
        display:block;
        float:left;
        cursor:pointer;
        margin-right:3px;
        font-size:20px;
        padding:3px;
        border:1px solid gray;
        border-right:0;
        text-align:center;
        width:23px;
        margin:0;
        color:gray;
        user-select: none;
    }
    .page-link:hover {
        background-color:#eee;
    }
    .lastpage {
        border-right:1px solid gray;
    }
    span.active {
        color:#346f83;
        font-weight:bold;
    }
    
</style>
