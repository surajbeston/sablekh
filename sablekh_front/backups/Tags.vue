<template>
    <div class="tags">
        <input type="text" v-model="tag_name" id="tag-name">
        <div class="show-tags" >
            <div v-bind:key="tag" v-for="tag in tags" class="each-tag">
                <span>{{tag}}</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tag_name: "",
            tags: ["science", "math"]
        }
    }
}
</script>

<style scoped>
    input {
        background-color: burlywood;
        border-radius: 5px;
    }
    .tags {
        width: 100vw;
    }
    .show-tags {
        width: 100%;
        display: flex;
    }
    .each-tag {
        padding: 10px;
    }
</style>