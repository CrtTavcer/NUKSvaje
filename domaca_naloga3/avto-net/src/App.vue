<template>
  <div class="container">
    <h1>Car Inventory</h1>
    <div v-if="cars.length">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Brand</th>
            <th>Model</th>
            <th>Year</th>
            <th>Mileage</th>
            <th>Price</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="car in cars" :key="car.id">
            <td>{{ car.id }}</td>
            <td>{{ car.brand }}</td>
            <td>{{ car.model }}</td>
            <td>{{ car.year }}</td>
            <td>{{ car.milage }}</td>
            <td>{{ car.price }}</td>
            <td><button @click="deleteCar(car.id)">Delete</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No cars found.</p>
    </div>
    <form>
      <h2>Add New Car</h2>
      <div>
        <label for="brand">Brand:</label>
        <input type="text" id="brand" v-model="newCar.brand">
      </div>
      <div>
        <label for="model">Model:</label>
        <input type="text" id="model" v-model="newCar.model">
      </div>
      <div>
        <label for="year">Year:</label>
        <input type="number" id="year" v-model.number="newCar.year">
      </div>
      <div>
        <label for="mileage">Mileage:</label>
        <input type="number" id="mileage" v-model.number="newCar.milage">
      </div>
      <div>
        <label for="price">Price:</label>
        <input type="number" id="price" v-model.number="newCar.price">
      </div>
      <button type="submit" @click.prevent="addCar">Add Car</button>
    </form>
  </div>
</template>

<script>
//import axios from 'axios'; //ne dela

export default {
  name: 'CarInventory',
  data() {
    return {
      cars: [],
      newCar: {
        brand: '',
        model: '',
        year: 0,
        milage: 0,
        price: 0,
      },
    };
  },
  
  mounted() {
   /*
    axios.get('http://localhost:8000/v2/list')
      .then((response) => {
        console.log("test");
        this.cars = response.data;
      })
      .catch((error) => {
        console.log("caught eror");
        console.error(error);
      });
  },
*/
  fetch('http://localhost:8000/v2/list', {
    method: 'GET',
    headers: {
        'Accept': 'application/json',
    },
    }).then(async (response) => {
      return response.json()
    }).then(response => {
      this.cars = response;
    })
    .catch((error) => {
      console.log(error.msg)
    })
  },
  
  
  methods: {
  getCars() {
    fetch('http://localhost:8000/v2/list', {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  })
  .then(response => response.json())
  .then(response => {
    this.cars = response;
  })
  .catch((error) => {
    console.log(error.msg)
  })
},

addCar() {
  fetch('http://localhost:8000/v2/add/car', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(this.newCar)
  })
  .then((response) => {
    console.log(response.data);
    this.getCars();
    this.clearForm();
  })
  .catch((error) => {
    console.error(error);
  });
    },
    
  deleteCar(id) {
  fetch(`http://localhost:8000/v2/delete/car/${id}`, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
    },
  })
    .then((response) => {
      console.log(response.data);
      this.getCars();
    })
    .catch((error) => {
      console.error(error);
    });
  },

    clearForm() {
      this.newCar.brand = '';
      this.newCar.model = '';
      this.newCar.year = 0;
      this.newCar.milage = 0;
      this.newCar.price = 0;
    },
  },
};
</script>