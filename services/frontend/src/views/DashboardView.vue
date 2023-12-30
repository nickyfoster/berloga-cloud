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
          <select name="type" v-model="form.type" class="form-control">
            <option v-for="type in types" :value="type" :key="type">{{ type }}</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="image" class="form-label">Image:</label>
          <select name="image" v-model="form.image" class="form-control">
            <option v-for="image in images" :value="image" :key="image">{{ image }}</option>
          </select>
        </div>
        <div v-if="!isServerCreating">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
        <div v-else>
          <button class="btn btn-primary" type="button" disabled>
            <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
            <span class="visually-hidden">Submit</span>
          </button>

        </div>
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
        name: null,
        type: "cx11",
        image: "ubuntu-22.04",
      },
      types: ["cx11"],
      images: ["ubuntu-22.04"],
    };
  },
  created: function () {
    return this.$store.dispatch('getServers');
  },
  computed: {
    ...mapGetters({ servers: 'stateServers', isServerCreating: 'isServerCreating' }),
  },
  methods: {
    ...mapActions(['createServer']),
    async submit() {
      await this.createServer(this.form);
    },
  },
});
</script>
