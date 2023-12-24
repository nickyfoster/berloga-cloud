<template>
  <section>
    <h1>Edit profile</h1>
    <hr /><br />
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="full_name" class="form-label">Full Name:</label>
        <input type="text" name="full_name" v-model="user.full_name" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" v-model="user.password" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="ssh_key" class="form-label">SSH Key:</label>
        <input type="text" name="ssh_key" v-model="user.ssh_key" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'EditUser',
  props: ['id'],
  data() {
    return {
      form: {
        full_name: '',
        password: '',
        ssh_key: ''
      },
    };
  },
  created: function () {
    this.GetUser();
  },
  computed: {
    ...mapGetters({ user: 'stateUser' }),
  },
  methods: {
    ...mapActions(['updateUser', 'viewUser']),
    async submit() {
      try {
        let user = {
          id: this.id,
          form: this.form,
        };
        await this.updateUser(user);
        this.$router.push({ name: 'Server', params: { id: this.user.id } });
      } catch (error) {
        console.log(error);
      }
    },
    async GetUser() {
      try {
        await this.viewMe(this.id);
        this.form.name = this.user.name;
        this.form.type = this.user.type;
      } catch (error) {
        console.error(error);
        this.$router.push('/dashboard');
      }
    }
  },
});
</script>
