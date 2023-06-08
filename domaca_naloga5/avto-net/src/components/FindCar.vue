<template>
    <div>
        <input class="id-input" type="text" v-model="carId" placeholder="Enter car image ID to display" />
        <button @click="getCarImageFromID()">Get Car Image</button>
        <img id="image-container" src="" />
    </div>
</template>

<script>
export default {
    name: "CarInventory",
    data() {
        return {
            cars: [],
            newCar: {
                brand: "",
                model: "",
                year: 0,
                milage: 0,
                price: 0,
            },
            updateCarId: null,
            formTitle: "Add New Car",
            submitButtonText: "Add Car",
            carId: 1, // Add this property to store the ID inputted by the user
        };
    },
    mounted() {
        this.getCarImageFromID();
    },
    methods: {
        getCarImageFromID() {
            const imageContainer = document.getElementById("image-container");
            imageContainer.innerHTML = ""; // Clear the image container
            const apiUrl = `http://212.101.137.121:8000/v2/get/img/${this.carId}`; // replace this with your own API endpoint to retrieve the binary image data

            fetch(apiUrl)
                .then((response) => response.json())
                .then((data) => {
                    // decode and display the image data
                    const imageData = data.image_data;
                    const imageSrc = `data:image/jpeg;base64,${imageData}`;
                    document.getElementById("image-container").src = imageSrc;
                })
                .catch((error) => console.error(error));
        },
    },
};
</script>

<style scoped>
/* IMG */
#image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    max-width: 400px;
    background-color: #f5f5f5;
}

#image-container img {
    max-width: 100%;
    max-height: 100%;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
}
/* INPUT */
.id-input {
    font-family: inherit;
    font-size: 16px;
    font-weight: 400;
    padding: 10px 15px;
    border: 2px solid #d6d6d6;
    border-radius: 5px;
    background-color: #f9f9f9;
    color: #333;
    transition: all 0.3s ease;
    max-width: 250px;
}

.id-input:focus {
    outline: none;
    border-color: #6dbdff;
    background-color: #fff;
    box-shadow: 0px 0px 5px rgba(109, 189, 255, 0.5);
}
</style>
