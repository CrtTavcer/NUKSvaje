<template>
    <div class="container">
        <form>
            <h2>{{ formTitle }}</h2>
            <div>
                <label for="brand">Brand:</label>
                <input type="text" id="brand" v-model="newCar.brand" />
            </div>
            <div>
                <label for="model">Model:</label>
                <input type="text" id="model" v-model="newCar.model" />
            </div>
            <div>
                <label for="year">Year:</label>
                <input type="number" id="year" v-model.number="newCar.year" />
            </div>
            <div>
                <label for="milage">Mileage:</label>
                <input type="number" id="milage" v-model.number="newCar.milage" />
            </div>
            <div>
                <label for="price">Price:</label>
                <input type="number" id="price" v-model.number="newCar.price" />
            </div>
            <button type="submit" @click.prevent="submitForm">{{ submitButtonText }}</button>
        </form>
        <table>
            <thead>
                <tr>
                    <th>Brand</th>
                    <th>Model</th>
                    <th>Year</th>
                    <th>Mileage</th>
                    <th>Price</th>
                    <th>Action</th>
                    
                </tr>
            </thead>
            <tbody>
                <tr v-for="car in cars" :key="car.id">
                    <td>{{ car.brand }}</td>
                    <td>{{ car.model }}</td>
                    <td>{{ car.year }}</td>
                    <td>{{ car.milage }}</td>
                    <td>{{ car.price }}</td>
                     
                    <td>
                        <button @click="editCar(car)">Edit</button>
                        <button @click="deleteCar(car.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <FindCar></FindCar>
    
        <AddImg></AddImg>

    </div>
</template>

<script>
import FindCar from "./components/FindCar.vue";
import AddImg from "./components/AddImg.vue";

export default {
    name: "CarInventory",
    components: {
        FindCar: FindCar,
        AddImg: AddImg,
    },
    data() {
        return {
            cars: [],
            newCar: {
                brand: "",
                model: "",
                year: 0,
                milage: 0,
                price: 0,
                //image: null,
            },
            updateCarId: null,
            formTitle: "Add New Car",
            submitButtonText: "Add Car",
        };
    },
    mounted() {
        this.getCars();
    },
    methods: {
        getCars() {
            fetch("http://localhost:8000/v2/list", {
                method: "GET",
                headers: {
                    Accept: "application/json",
                },
            })
                .then((response) => response.json())
                .then((response) => {
                    this.cars = response;
                })
                .catch((error) => {
                    console.log(error.msg);
                });
        },
        addCar() {
            fetch("http://localhost:8000/v2/add/car", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(this.newCar),
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
        updateCar(id, brand) {
            fetch(`http://localhost:8000/v2/update/car/${id}/${brand}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(this.newCar),
            })
                .then((response) => {
                    console.log(response.data);
                    this.getCars();
                    this.clearForm();
                    this.formTitle = "Add New Car";
                    this.submitButtonText = "Add Car";
                    this.updateCarId = null;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        editCar(car) {
            this.newCar = Object.assign({}, car);
            this.formTitle = "Edit Car";
            this.submitButtonText = "Update Car";
            this.updateCarId = car.id;
        },
        submitForm() {
            if (this.updateCarId) {
                this.updateCar(this.updateCarId);
            } else {
                this.addCar();
            }
        },
        clearForm() {
            this.newCar.brand = "";
            this.newCar.model = "";
            this.newCar.year = 0;
            this.newCar.milage = 0;
            this.newCar.price = 0;
        },
        deleteCar(id) {
            fetch(`http://localhost:8000/v2/delete/car/${id}`, {
                method: "DELETE",
                headers: {
                    Accept: "application/json",
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
    },
};
</script>

<style>
/* Global styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    background-color: #9e9797;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* Form styles */
form {
    background-color: #fff;
    border-radius: 5px;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h2 {
    font-size: 24px;
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 10px;
}

input[type="text"],
input[type="number"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: none;
    border-radius: 5px;
    background-color: #f5f5f5;
    font-size: 16px;
}

input[type="submit"] {
    display: block;
    margin: 0 auto;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #4caf50;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

input[type="submit"]:hover {
    background-color: #3e8e41;
}

/* Table styles */
table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
}

thead th,
tbody td {
    padding: 10px;
    text-align: left;
}

thead th {
    background-color: #333;
    color: #fff;
}

tbody tr:nth-child(even) {
    background-color: #f2f2f2;
}

tbody td:last-child {
    text-align: center;
}

tbody button {
    padding: 10px;
    border: none;
    border-radius: 5px;
    background-color: #2196f3;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 10px;
}

tbody button:hover {
    background-color: #0b7dda;
}

tbody button:last-child {
    background-color: #f44336;
}

tbody button:last-child:hover {
    background-color: #da190b;
}
</style>
