<template>
    <div>
      <form @submit.prevent="uploadCarImg">
        <label>
          Select Car Image:
          <input type="file" ref="fileInput" />
        </label>
        <button type="submit">Upload</button>
      </form>
      <button @click="deleteCarImg">Delete Image</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      async uploadCarImg() {
        const fileInput = this.$refs.fileInput;
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);
  
        try {
          const response = await fetch("http://localhost:8000/add/car/img", {
            method: "POST",
            body: formData,
          });
          const data = await response.json();
          console.log(data);
        } catch (error) {
          console.log(error);
        }
      },
      async deleteCarImg() {
        const id = 1; // Replace with the ID of the image you want to delete
        try {
          const response = await fetch(`http://localhost:8000/delete/car/img/${id}`, {
            method: "DELETE",
          });
          const data = await response.json();
          console.log(data);
        } catch (error) {
          console.log(error);
        }
      },
    },
  };
  </script>

  
<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

.label {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.input {
  padding: 10px;
  border-radius: 5px;
  border: none;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

.button {
  padding: 10px 20px;
  margin-top: 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease-in-out;
}

.button:hover {
  background-color: #0069d9;
}

.delete-button {
  margin-top: 10px;
  background-color: #dc3545;
}

.delete-button:hover {
  background-color: #c82333;
}
</style>