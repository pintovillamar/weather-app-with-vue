<template>
  <v-card class="mx-auto" max-width="680">
    <v-card-item>
      <v-text-field v-model="searchText" placeholder="Search for a city"></v-text-field>
      <v-btn color="primary" @click="searchCity()">Search</v-btn>
      <v-btn color="primary" @click="getUserLocation()">usar mi localización</v-btn>
      <v-btn color="primary" @click="switchFarenheit()">F°</v-btn>
    </v-card-item>
    <v-card-item :title="'Resultados para: ' + searchCityText">
      <template v-slot:subtitle v-if="extreme_weather">
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
            {{ temp }}
          </template>
        </v-col>
        <v-col cols="6" class="text-right">
          <v-icon :color="primary" :icon="weatherIcon" size="88"></v-icon>
        </v-col>
      </v-row>
    </v-card-text>

  </v-card>
</template>

<script>
import axios from 'axios'
import sunnyIcon from '@/assets/sun.svg';
import coldIcon from '@/assets/cold.svg';
export default {
  data: () => ({
    URL: 'http://localhost:5001',
    searchText: '',
    searchCityText: '',
    temp: '',
    f_temp: 0,
    extreme_weather: false,
    isLoadingTemp: false,
    icon: '',
    iconColor: '',
    isFarenheit: false,
    isCelsius: true,
    weatherIcon: ''

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
          this.ifExtreme(this.temp);
          this.isLoadingTemp = false;
        })
        .catch((error) => {
          console.log(error)
          this.isLoadingTemp = false;
        })
    },

    ifExtreme: function (temp) {
      if (temp > 40 || temp < -9) {
        this.extreme_weather = true;
      } else {
        this.extreme_weather = false;
      }
    },

    searchCity: function () {
      if (this.searchText === '') {
        return;
      }

      const endpoint = '/test_city2/' + this.searchText;

      this.getWeatherData(endpoint);
      this.searchCityText = this.searchText;
    },

    getUserLocation: function () {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          const endpoint = `/get_city_name/${position.coords.latitude}/${position.coords.longitude}`;
          axios.get(this.URL + endpoint)
            .then((response) => {
              console.log(response.data);
              this.searchCityText = response.data.city_name;
              this.getWeatherData(`/test_coord/${position.coords.latitude}/${position.coords.longitude}`);
            })
            .catch((error) => {
              console.log(error);
              this.isLoadingTemp = false;
            });
        });
      } else {
        console.log("Geolocation is not supported by this browser.");
      }
    },

    switchFarenheit: function () {
      if (this.temp === '') {
        return;
      }
      if (this.isCelsius) {
        this.temp = parseFloat(this.temp) * 9 / 5 + 32;
      } else {
        this.temp = (parseFloat(this.temp) - 32) * 5 / 9;
      }
      this.temp = this.temp.toFixed(0);
      this.isCelsius = !this.isCelsius;
    },

    computed: {
      weatherIcon() {
        if (this.temp >= 15) {
          return sunnyIcon;
        } else {
          return coldIcon;
        }
      }
    },


    mounted() {
      const endpoint = '/test_temp';
      this.getWeatherData(endpoint);
      this.ifExtreme(this.temp);
      this.getUserLocation();
    }
  }
}
</script>
<style>
body {
  background: url("https://www.abc27.com/wp-content/uploads/sites/55/2022/10/GettyImages-1125295327.jpg?w=2560&h=1440&crop=1") no-repeat center center fixed;
  background-size: cover;
}
</style>