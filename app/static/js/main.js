
function toggle (element){
    if(element.classList.contains('active')){
        element.classList.remove('active')
        element.style.backgroundColor = ''
    }else{
        element.classList.add('active')
        element.style.backgroundColor = ('rgb(20.83,45, 1)')
    }
}

function toggleDescription (description){
    if(description.classList.contains('active')){
        description.classList.remove('active')
        description.style.color = ('rgb(107, 114, 128, 1)')
    }else{
        description.classList.add('active')
        description.style.color = ('rgb(255, 255, 255, 1)')
    }
}

function toggleCheck (checkbox){
    checkbox.checked = !checkbox.checked
}

document.addEventListener('DOMContentLoaded', () => {
    body = document.querySelectorAll('.body-div')
    checkbox = document.querySelectorAll('.checked')
    body.forEach(element => {
        element.addEventListener('click', () => {
            toggle(element)
            const check = element.querySelector('.checked')
            const description = element.querySelector('.description')
            toggleCheck(check)
            toggleDescription(description)
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
