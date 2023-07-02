const { createApp } = Vue
  createApp({
    data() {
      return {
        categorias:[],
        url:'http://localhost:5000/categorias', 
        error:false,
        cargando:true,
        /*atributos para el guardar los valores del formulario */
        id:0,
        categoria:"", 
        detalle:"",
    }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.categorias = data;
                    this.cargando=false
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        eliminar(categoria) {
            const url = this.url+'/' + categoria;
            var options = {
                method: 'DELETE',
            }
            fetch(url, options)
                .then(res => res.text()) // or res.json()
                .then(res => {
                    location.reload();
                })
        },
        grabar(){
            let categoria = {
                categoria:this.categoria,
                detalle: this.detalle,
            }
            var options = {
                body:JSON.stringify(categoria),
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro grabado")
                    window.location.href = "./categorias.html";  
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Grabarr")
                })      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')