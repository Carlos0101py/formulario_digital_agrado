
function toggle (element){
    if(element.classList.contains('active')){
        element.classList.remove('active')
        element.style.backgroundColor = ''
    }else{
        element.classList.add('active')
        element.style.backgroundColor = ('rgb(20.83,45, 1)')
    }
}

function toggleCheck (checkbox){
    checkbox.checked = !checkbox.checked
    if(checkbox.checked){
        console.log('marcado')
    }else{
        console.log('desmarcado')
    }
}

document.addEventListener('DOMContentLoaded', () => {
    body = document.querySelectorAll('.body-div')
    checkbox = document.querySelectorAll('.checked')
    body.forEach(element => {
        element.addEventListener('click', () => {
            toggle(element)
            const check = element.querySelector('.checked')
            toggleCheck(check)
        });
    });
});

// function toggle (element, color) {
//     if(element.classList.contains('active') ){
//         element.classList.remove('active')
//         element.style.backgroundColor = 'rgb(71,85,105,1)'
//     }else{
//         element.classList.add('active')
//         element.style.backgroundColor = color
//     }
// }

// document.addEventListener('DOMContentLoaded', () => {
//     back = document.querySelectorAll('.corpo-div')
//     back.forEach(a => {
//         a.addEventListener('click', () => {
//             toggle(a, 'red')
//         })
//     })
// });
