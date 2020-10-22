<template>
  <div class="note-form">

    <label for="category">Category: </label>
    <input type="checkbox" name="category" v-model="categories" true-value="yes" false-value="no">
  </div>
</template>

<script>
export default {
  name: 'NoteForm',
  categories: ['personal', 'business']
}
</script>

<style scoped>
</style>
