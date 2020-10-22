<template>
  <div class="authentication">

    <label for="username">Username: </label>
    <input type="text" name="username" v-model="username">

    <label for="password">Password: </label>
    <input type="text" name="password" v-model="password">

  </div>
</template>

<script>
export default {
  name: 'Authentication',
  props: {
    username: String,
    password: String
  }
}
</script>

<style scoped>

.authentication {

  display: flex;
  flex-flow: row nowrap;
  justify-content: flex-start;
}

label {
  margin: 0 5px;
}


</style>
