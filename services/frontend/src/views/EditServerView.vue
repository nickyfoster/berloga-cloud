<template>
  <section>
    <h1>Edit server</h1>
    <hr /><br />
    <p>TODO update same as DashboardView</p>

    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="name" class="form-label">Name:</label>
        <input type="text" name="name" v-model="form.name" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="type" class="form-label">Type:</label>
        <input type="text" name="type" v-model="form.type" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'EditServer',
  props: ['id'],
  data() {
    return {
      form: {
        name: '',
        type: '',
      },
    };
  },
  created: function () {
    this.GetServer();
  },
  computed: {
    ...mapGetters({ server: 'stateServer' }),
  },
  methods: {
    ...mapActions(['updateServer', 'viewServer']),
    async submit() {
      try {
        let server = {
          id: this.id,
          form: this.form,
        };
        await this.updateServer(server);
        this.$router.push({ name: 'Server', params: { id: this.server.id } });
      } catch (error) {
        console.log(error);
      }
    },
    async GetServer() {
      try {
        await this.viewServer(this.id);
        this.form.name = this.server.name;
        this.form.type = this.server.type;
      } catch (error) {
        console.error(error);
        this.$router.push('/dashboard');
      }
    }
  },
});
</script>
