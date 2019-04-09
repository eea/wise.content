<template>
    <div class="paginator-container">
        <div class="paginator">
            <div style="clear:both"></div>
                <div v-if="pos > 0" class="prev-page-link" @click="goToPrevPage">Previous</div>
                <PaginatorPage v-for="page in pages" :page="page" @pageChanged="pageChanged" :batch_size="batch_size" :pos="pos" :current_page="current_page" :count="pages.length" :key="page"></PaginatorPage>
                <div v-if="current_page < pages.length " class="next-page-link" @click="goToNextPage">Next</div>
            <div style="clear:both"></div>
        </div>
    </div>
</template>

<script>

import PaginatorPage from './PaginatorPage.vue';

export default {

    components: { PaginatorPage },

    props: [ 'count', 'pos', 'batch_size' ],
    data() {
        return {}
    },
    computed: {
        pages(){
            var page_nr =  Math.ceil(this.count / this.batch_size);
            var tmp_pages = [];
            for (var i = 0; i < page_nr; i++){
                tmp_pages.push(i+1);
            }
            return tmp_pages;
        },
        current_page() {
            return this.pos / this.batch_size + 1;
        }
    },
    methods: {
        goToPrevPage(){
            this.$emit("pageChanged", this.pos / this.batch_size)
        },
        goToNextPage(){
            this.$emit("pageChanged", this.pos / this.batch_size + 2)
        },
        pageChanged(page) {
            this.$emit("pageChanged", page);
        }
    }
}

</script>

<style>
    .paginator-container {
        width:100%;
        text-align:center;
    }
    .paginator {
        display:inline-block;
    }
    .prev-page-link,
    .next-page-link {
        display:block;
        float:left;
        cursor:pointer;
        margin-right:3px;
        font-size:20px;
        border:1px solid gray;
        padding:3px;
        text-align:center;
        margin:0;
        color:gray;
        padding-left:10px;
        padding-right:10px;
        user-select: none;
    }
    .prev-page-link:hover,
    .next-page-link:hover {
            background-color:#eee;
    }

    .prev-page-link{
        border-right:0;
    }

</style>
