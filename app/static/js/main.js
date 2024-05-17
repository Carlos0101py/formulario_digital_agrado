
function toggle (element){
    if(element.classList.contains('active')){
        element.classList.remove('active')
        element.style.backgroundColor = ''
        element.style.color = ('rgb(107, 114, 128, 1)')
    }else{
        element.classList.add('active')
        element.style.backgroundColor = ('#14532D')
        element.style.color = ('rgb(255, 255, 255, 1)')
    }
}

function toggleCheck (checkbox){
    checkbox.checked = !checkbox.checked
}

function hiddenNotification(element){
    element.style.display = "none";
}

document.addEventListener('DOMContentLoaded', ()=>{
    notification = document.querySelector('.notification_div')

    if(notification != null){
        setTimeout(()=> hiddenNotification(notification), 5000)
    }
})


document.addEventListener('DOMContentLoaded', () => {
    body = document.querySelectorAll('.body-div')
    checkbox = document.querySelectorAll('.checked')

    body.forEach(element => {
        element.addEventListener('click', () => {
            const check = element.querySelector('.checked')
            const description = element.querySelector('.description')
            toggleCheck(check)
            toggle(element)
            toggle(description)
        });
    });
});


document.addEventListener('DOMContentLoaded', () =>{
    body = document.getElementById('anexoBody')
    inputFile = document.getElementById('anexo')
    parquivo = document.getElementById('NomeArquivo')

    body.addEventListener('click', () =>{

        inputFile.click()

        inputFile.addEventListener('change', ()=>{

            const curFile = inputFile.files

            body.style.backgroundColor= '#14532D'
            
            for (file of curFile){
                parquivo.textContent = file.name
            }
        })
    })
})