console.log("Hola que hace")

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')
const url = window.location.href
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', () => {
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-test')
    const numQuestions = modalBtn.getAttribute('data-questions')

    modalBody.innerHTML = `
        <div class="h5 mb-3"> Test de Escala de Estrés</div>
        <div class="text-muted">
            <ul>
                <li>Número de Preguntas: <b>${numQuestions}</b></li>
            </ul>
         </div> 
   `
    startBtn.addEventListener('click', () => {
         window.location.href = url+ pk
    })
}))