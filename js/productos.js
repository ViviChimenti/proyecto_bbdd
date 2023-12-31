const { createApp } = Vue
  createApp({
    data() {
      return {
        productos:[],
        categorias: [],  //agregué esto para probar el desplegable
        url:'http://localhost:5000/productos', 
        urlCategorias: 'http://localhost:5000/categorias', // agregué esto, URL para obtener las categorías
        error:false,
        cargando:true,
        /*atributos para el guardar los valores del formulario */
        id:0,
        nombre:"", 
        imagen:"",
        stock:0,
        precio:0,
       
     }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.productos = data; 
                    this.cargando=false
                })
                
                .catch(err => {
                    console.error(err);
                    this.error=true              
                });

       
        },

        // 
        fetchCategorias(urlCategorias) {
            fetch(urlCategorias)
              .then(response => response.json())
              .then(data => {
                this.categorias = data;
                const nuevoElemento = { id: 1, categoria: "Seleccione opción" }; // Ejemplo de nuevo elemento
                data.unshift(nuevoElemento);
              })
              .catch(err => {
                console.error(err);
                this.error = true;
              });
          },
        // 

        eliminar(producto) {
            Swal.fire({
                title: '¿Estás seguro?',
                text: "¡No podrás revertir esto!",
                icon: 'Advertencia',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: '¡Sí, elimínalo!'
              }).then((result) => {
                if (result.isConfirmed) {
                    const url = this.url+'/' + producto;
                        var options = {
                            method: 'DELETE',
                        }
                        fetch(url, options)
                            .then(res => res.text()) // or res.json()
                            .then(res => {
                                location.reload();
                        })
                }
              })
        },
        grabar(){
            let producto = {
                nombre:this.nombre,
                precio: this.precio,
                stock: this.stock,
                pcategoria:this.pcategoria,
                imagen:this.imagen
                
            }
            var options = {
                body:JSON.stringify(producto),
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro grabado")
                    window.location.href = "./productos.html";  
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Grabarr")
                })      
        }


    },
    created() {
        this.fetchData(this.url);
        this.fetchCategorias(this.urlCategorias);
    },



    
  }).mount('#app');


