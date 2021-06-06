console.log('hola que hace test')
const url = window.location.href
const testBox = document.getElementById('test-box')
console.log(url)
//Inyectar el pk en un div con id hiden
$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function (response) {
        console.log(response)
        let data = response.data
        data.forEach(el => {
            for (const [pregunta, respuestas] of Object.entries(el)) {
                testBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${pregunta}</b>
                    </div>
                `
                respuestas.forEach(respuesta => {
                    testBox.innerHTML += `
                        <div>
                            <input type="radio" class="res" id="${pregunta}-${respuesta}" name="${pregunta}" value="${respuesta}">
                            <label for="${pregunta}">${respuesta}</label>
                        </div>
                    `
                })
            }
        });
    },
    error: function (error) {
        console.log(error)
    }
})

const testForm = document.getElementById('test-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

//mandar el pk
const sendData = () => {
    const elements = [...document.getElementsByClassName('res')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if (el.checked) {
            data[el.name] = el.value
        } else {
            if (!data[el.name]) {
                data[el.name] = null
            }
        }
    })
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function (response) {
            console.log(response)
            window.location.href = "/";
        },
        error: function (error) {
            console.log(error)
        }
    })
}

testForm.addEventListener('submit', e => {
    e.preventDefault()
    sendData()
    location.href("/")
    //window.location.replace("../../diario") 
    //window.location.replace(url+"../../diario")
})