<template>
  <v-card class="mx-auto" max-width="680">
    <v-card-item>
      <v-text-field v-model="searchText" placeholder="Search for a city"></v-text-field>
      <v-btn color="primary" @click="searchCity()">Search</v-btn>
    </v-card-item>
    <v-card-item :title="'Resultados para: ' + searchCityText">
      <template v-slot:subtitle v-if="checker">
        <v-icon icon="mdi-alert" size="18" color="error" class="me-1 pb-1"></v-icon>
        Extreme Weather Alert
      </template>
    </v-card-item>

    <v-card-text class="py-0">
      <v-row align="center" no-gutters>
        <v-col class="text-h2" cols="6">
          <template v-if="isLoadingTemp">
            <v-progress-circular indeterminate color="black"></v-progress-circular>
          </template>
          <template v-else>
            {{ temp }}&deg;C
          </template>
        </v-col>
        <v-col cols="6" class="text-right">
          <v-icon :color="iconColor" :icon="icon" size="88"></v-icon>
        </v-col>
      </v-row>
    </v-card-text>

  </v-card>
</template>

<script>
import axios from 'axios'
export default {
  data: () => ({
    URL: 'http://localhost:5000',
    searchText: '',
    searchCityText: '',
    temp: '',
    checker: false,
    isLoadingTemp: false,
    icon: '',
    iconColor: '',
  }),

  methods: {
    getWeatherData: function (endpoint) {
      this.isLoadingTemp = true;
      axios.get(this.URL + endpoint)
        .then((response) => {
          console.log(response.data)
          this.temp = response.data.temp_cel;
          this.icon = response.data.icon;
          this.iconColor = response.data.iconColor;
          this.isLoadingTemp = false;
        })
        .catch((error) => {
          console.log(error)
          this.isLoadingTemp = false;
        })
    },

    searchCity: function () {
      if (this.searchText === '') {
        return;
      }

      const endpoint = '/test_city2/' + this.searchText;

      this.getWeatherData(endpoint);
      this.searchCityText = this.searchText;
    },
  },

  mounted() {
    const endpoint = '/test_temp';
    this.getWeatherData(endpoint);
  }
}
</script>