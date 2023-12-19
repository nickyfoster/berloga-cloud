<template>
  <div>
    <section>
      <h1>Create server</h1>
      <hr /><br />

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="name" class="form-label">Name:</label>
          <input type="text" name="name" v-model="form.name" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="type" class="form-label">Type:</label>
          <textarea name="type" v-model="form.type" class="form-control"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </section>

    <br /><br />

    <section>
      <h1>Servers</h1>
      <hr /><br />

      <div v-if="servers.length">
        <div v-for="server in servers" :key="server.id" class="servers">
          <div class="card" style="width: 18rem;">
            <div class="card-body">
              <ul>
                <li><strong>Name:</strong> {{ server.name }}</li>
                <li><strong>Type:</strong> {{ server.type }}</li>
                <li><router-link :to="{ name: 'Server', params: { id: server.id } }">View</router-link></li>
              </ul>
            </div>
          </div>
          <br />
        </div>
      </div>

      <div v-else>
        <p>Nothing to see. Check back later.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'DashboardView',
  data() {
    return {
      form: {
        name: '',
        type: '',
      },
    };
  },
  created: function () {
    return this.$store.dispatch('getServers');
  },
  computed: {
    ...mapGetters({ servers: 'stateServers' }),
  },
  methods: {
    ...mapActions(['createServer']),
    async submit() {
      await this.createServer(this.form);
    },
  },
});
</script>
