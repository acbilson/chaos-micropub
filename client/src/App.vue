<template>
  <div id="app">
    <Authentication />
    <NoteForm />
  </div>

</template>

<script>
import Authentication from './components/Authentication.vue'
import NoteForm from './components/NoteForm.vue'

export default {
  name: 'App',
  components: {
    Authentication,
    NoteForm
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
}
</style>
