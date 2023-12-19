<template>
  <section>
    <p>Berloga Cloud - fast & private personal cloud</p>

    <div v-if="isLoggedIn" id="logout">
      <p id="logout">Click <a href="/dashboard">here</a> to view all servers.</p>
    </div>
  </section>
</template>
<script>

import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isAuthenticated;
    }
  },
});
</script>
