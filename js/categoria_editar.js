console.log(location.search)     // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
  createApp({
    data() {
      return {
        id:0,
        categoria:"",
        detalle:"",
        url:'http://localhost:5000/categorias/'+id,
       }  
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    this.id=data.id
                    this.categoria = data.categoria;
                    this.detalle=data.detalle                    
                })
                .catch(err => {
                    console.error(err);
                    this.error=true              
                })
        },
        modificar() {
            console.log(this.categoria)
            let categoria = {
                categoria:this.categoria,
                detalle: this.detalle,
            }
            var options = {
                body: JSON.stringify(categoria),
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                redirect: 'follow'
            }
            fetch(this.url, options)
                .then(function () {
                    alert("Registro modificado")
                    window.location.href = "./categorias.html";             
                })
                .catch(err => {
                    console.error(err);
                    alert("Error al Modificar")
                })      
        }
    },
    created() {
        this.fetchData(this.url)
    },
  }).mount('#app')